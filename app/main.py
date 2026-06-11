import time

from fastapi import FastAPI, HTTPException
from langgraph.graph import END, StateGraph
from models import DocumentRequest, QuestionRequest
from repositories.docs_repository import DocsRepository
from repositories.qdrant_repository import QdrantRepository

app = FastAPI(title="Learning RAG Demo")

# Qdrant setup (assumes local instance)
try:
    qdrant = QdrantRepository(collection_name="demo_collection")
    USING_QDRANT = True
except Exception as e:
    print("⚠️  Qdrant not available. Falling back to in-memory list.")
    memory_list = DocsRepository()
    USING_QDRANT = False


# LangGraph state = plain dict
def simple_retrieve(state):
    query = state["question"]

    if USING_QDRANT:
        results = qdrant.retrieve(query)
    else:
        results = memory_list.retrieve(query)

    state["context"] = results
    return state


def simple_answer(state):
    ctx = state["context"]
    if ctx:
        answer = f"I found this: '{ctx[0][:100]}...'"
    else:
        answer = "Sorry, I don't know."
    state["answer"] = answer
    return state


# Build graph
workflow = StateGraph(dict)
workflow.add_node("retrieve", simple_retrieve)
workflow.add_node("answer", simple_answer)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "answer")
workflow.add_edge("answer", END)
chain = workflow.compile()


# --- API ENDPOINTS ---
@app.post("/ask")
def ask_question(req: QuestionRequest):
    start = time.time()
    try:
        result = chain.invoke({"question": req.question})
        return {
            "question": req.question,
            "answer": result["answer"],
            "context_used": result.get("context", []),
            "latency_sec": round(time.time() - start, 3),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add")
def add_document(req: DocumentRequest):
    try:
        doc_id: int
        if USING_QDRANT:
            doc_id = qdrant.add(req.text)
        else:
            doc_id = memory_list.add(req.text)

        return {"id": doc_id, "status": "added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
def status():
    return {
        "qdrant_ready": USING_QDRANT,
        "in_memory_docs_count": len(memory_list),
        "graph_ready": chain is not None,
    }
