🧩 Code Quality Exercise 

For Associate Software Engineer Candidates 

Thank you for your interest in joining our team! As part of our technical evaluation, we invite you to review and refactor the small Python application in this repository. 

This exercise is designed to assess your understanding of code structure, maintainability, and software design fundamentals—not just whether the code runs. 

📌 The Task 

We’ve provided a working but intentionally unstructured implementation of a simple RAG (Retrieval-Augmented Generation) service using: 

    FastAPI  
    LangGraph  
    Qdrant (with in-memory fallback)
     

Your goal:
Refactor the code into a cleaner, more maintainable, and production-suitable structure using object-oriented principles and good software engineering practices. 

You are not expected to add new features, only to improve the internal design while preserving existing behavior. 
 
📁 What’s Included 

    main.py: A single-file implementation that works but contains common anti-patterns (e.g., global state, tight coupling, lack of separation of concerns).
    README.md: Instructions and context.
 
✅ What We’re Looking For 

We want to see how you think about code quality. In your refactored version, prioritize: 

    Encapsulation: Group related data and behavior together.
    Separation of concerns: Split web logic, business logic, and data access.
    Explicit dependencies: Avoid global variables; pass what you need.
    Testability: Structure code so units can be validated in isolation.
    Readability: Clear naming, logical structure, minimal surprise.
     

    💡 You don’t need to implement unit tests—but design the code so they could be added easily. 
     
🛠 How to Approach This 

    Understand the current behavior
    Run the app, try the endpoints (/add, /ask), and confirm you know what it does. 

    Identify key responsibilities   
        Handling HTTP requests  
        Managing document storage (Qdrant or fallback)  
        Generating fake embeddings  
        Executing the retrieval → answer workflow

    Redesign around these responsibilities
    Consider creating classes like: 
        EmbeddingService
        DocumentStore
        RagWorkflow
        API router or controller

    Refactor incrementally
    Keep the same external API—only change the internal structure. 

 
📤 Submission Guidelines 

Please provide: 
    A refactored version of the code (you may split into multiple files)
    A short README.md (1–3 paragraphs) explaining:
        Your main design decisions
        One trade-off you considered
        How your version improves maintainability
         

Submit via github repo with public link.
 

Note: This is not a test of your knowledge of LangGraph or Qdrant—we’re evaluating how you organize code, manage dependencies, and apply basic OOP principles in a realistic context. 
     
Good luck—and we look forward to seeing your approach!
