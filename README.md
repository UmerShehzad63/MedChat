# Medical ChatBot (MedChat)

## Overview
The Medical ChatBot (MedChat) is a premium, evidence-based medical information application. It leverages advanced natural language processing (NLP) techniques, including Retrieval-Augmented Generation (RAG), to answer user queries with high accuracy and reliability. The chatbot integrates with a local FAISS vector database for efficient document retrieval from the GALE Encyclopedia of Medicine and uses a pre-trained language model from OpenAI to generate structured, clinical responses.

Initially conceived as a Streamlit application, MedChat has been completely overhauled with a bespoke Flask backend and a custom HTML/CSS frontend to deliver a high-end, $200/month medical SaaS aesthetic.

## Features
*   **Premium Interactive Interface:** A polished, "Linear-style" custom HTML/CSS frontend featuring a three-zone layout (Left Rail, Chat Area, Sticky Input), responsive design, and sophisticated micro-interactions.
*   **Retrieval-Augmented Generation (RAG):** Combines dense vector document retrieval with advanced language generation to provide accurate, context-aware answers.
*   **Local Vector Database:** Utilizes FAISS for lightning-fast similarity search and retrieval of document embeddings.
*   **Evidence-Based Clinical Responses:** The chatbot strictly adheres to the provided medical literature, avoiding unsupported claims. Responses are structured with "Clinical Answer" and "Supporting Evidence" sections.
*   **Source Citing & Confidence:** Every response includes detailed source attribution (document name and page number) and an explicit Confidence Score (High, Medium, Low).
*   **Flask API Backend:** A robust, lightweight Python Flask server handles the routing, UI serving, and LLM communication.

## Technologies Used
1.  **Flask**
    A micro web framework written in Python. Used to serve the web application and handle API requests from the frontend.
2.  **LangChain**
    A framework for building applications powered by large language models (LLMs). Used to orchestrate the RAG pipeline.
3.  **OpenAI GPT-4o-mini**
    A fast, state-of-the-art large language model developed by OpenAI, providing intelligent, structured natural language text generation.
4.  **HuggingFace Transformers**
    Provides the `sentence-transformers/all-MiniLM-L6-v2` model for embedding generation. This model is lightweight and highly optimized for semantic similarity.
5.  **FAISS (Facebook AI Similarity Search)**
    A library for efficient similarity search and clustering of dense vectors. Used as the local vector store.
6.  **HTML5 / Vanilla CSS**
    Used to craft the bespoke, highly styled dark-mode user interface.
7.  **Python**
    The primary backend programming language.

## Project Structure
```text
medchat/
├── app.py                      # Flask web server and backend API routing
├── connect_llm_with_memory.py  # Core LangChain RAG pipeline & initialization
├── memory_for_llm.py           # Vector database creation utility
├── templates/
│   └── index.html              # Custom premium medical UI (HTML/CSS/JS)
├── data/                       # Directory for storing raw data (e.g., GALE PDF)
├── DB_FAISS/                   # FAISS vector database index files
├── .env                        # Environment variables (OpenAI API Key)
└── requirements.txt            # Python dependencies
```

## How It Works
1.  **Document Embedding and Storage:**
    The application uses the `sentence-transformers/all-MiniLM-L6-v2` model from HuggingFace to generate embeddings for PDFs placed in the `data/` folder. These embeddings are persisted locally in a FAISS vector database.
2.  **Query Processing:**
    When a user submits a question via the web interface, the query is passed to the Flask backend, which triggers a custom `LocalMultiQueryRetriever` to generate multiple semantic perspectives on the question to ensure comprehensive retrieval.
3.  **Response Generation:**
    The retrieved document chunks are passed to the `gpt-4o-mini` model along with a strict system prompt. The model generates a structured Markdown response detailing the answer, quotes, limitations, confidence, and source citations.
4.  **Formatting and UI Render:**
    The Flask backend intercepts the Markdown, strips raw metadata tags, and wraps the sections in custom CSS classes before sending it as an HTML payload back to the browser.
5.  **Caching:**
    The LangChain `LocalMultiQueryRetriever` incorporates LLMCache mechanisms internally, while FAISS models are loaded into application memory on server start for speed.

## How to Run the Application

### 1. Install Dependencies
Ensure you have Python 3.9+ installed on your system. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory and add your OpenAI API key:
```env
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Prepare the Vector Database (If starting fresh)
Place your reference medical documents (e.g., PDFs) in the `data/` directory. Run the memory initialization script to parse these files and build the FAISS index:
```bash
python memory_for_llm.py
```

### 4. Run the Flask Server
Start the backend application server:
```bash
python app.py
```

### 5. Interact with the ChatBot
Open your web browser and navigate to:
```text
http://localhost:5000
```

## Future Improvements
*   **Enhanced Data Sources:** Integrate larger, up-to-date medical datasets or trusted medical APIs (like PubMed).
*   **Persistent Chat Sessions:** Add browser local storage or server-side session management to maintain conversational history across page reloads.
*   **User Authentication:** Add login systems to provide personalized experiences and save user histories securely.
*   **Mobile Optimization:** Further refine the CSS to ensure perfect semantic scaling and touch targets on narrow viewports.
*   **Cloud Deployment:** Containerize the application using Docker and deploy to platforms like AWS ECS or Google Cloud Run.

## License
This project is for educational purposes. 

## Acknowledgments
*   **Flask** for the robust web server framework.
*   **LangChain** for the retrieval-augmented generation pipeline orchestration.
*   **HuggingFace** for the open-source embedding models.
*   **FAISS** for rapid vector indexing.
*   **OpenAI** for the powerful GPT-4o-mini language model.