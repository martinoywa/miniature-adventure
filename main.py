import streamlit as st
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# Predefined dataset
qa_data = [
        {
            "question": "What does the eligibility verification agent (EVA) do?",
            "answer": "EVA automates the process of verifying a patient’s eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
        },
        {
            "question": "What does the claims processing agent (CAM) do?",
            "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
        },
        {
            "question": "How does the payment posting agent (PHIL) work?",
            "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
        },
        {
            "question": "Tell me about Thoughtful AI's Agents.",
            "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
        },
        {
            "question": "What are the benefits of using Thoughtful AI's agents?",
            "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
        }
]


# Build Vector Store for Hardcoded Q&A
embeddings = OllamaEmbeddings(model="nomic-embed-text")
documents = [Document(page_content=qa["question"], metadata={"answer": qa["answer"]}) for qa in qa_data]
vectorstore = FAISS.from_documents(documents, embeddings)


# Ollama LLM (fallback)
llm = OllamaLLM(model="llama3.1:latest")


# Helper function
def get_answer(user_input: str, threshold: float = 0.50) -> str:
    """
    Uses similarity search on hardcoded dataset first with a threshold.
    Falls back to Ollama LLM if no relevant match is found.
    """
    try:
        if not user_input or not user_input.strip():
            return "I didn’t catch that. Could you rephrase your question?"

        # Search FAQs with score
        results = vectorstore.similarity_search_with_score(user_input, k=1)

        if results:
            best_match, score = results[0]
            similarity = 1 - score

            if similarity >= threshold and best_match.metadata.get("answer"):
                return best_match.metadata["answer"]

        # Fallback
        response = llm.invoke(user_input)
        return response

    except Exception as e:
        return f"Oops, something went wrong: {str(e)}"


# Streamlit UI
st.title("Thoughtful AI Support Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Ask me about Thoughtful AI..."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response
    answer = get_answer(user_input)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)