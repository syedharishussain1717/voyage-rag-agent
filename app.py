
import uuid
from pathlib import Path

import streamlit as st

from modules.pdf_loader import load_and_split_pdf
from modules.vector_store import (
    create_vector_store,
    load_vector_store
)
from modules.agent import create_voyage_agent


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MEMORY_DB = BASE_DIR / "voyage_memory.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="VoyageAI - Smart Travel Assistant",
    page_icon="✈️",
    layout="wide"
)


# --------------------------------------------------
# CACHED AGENT INITIALIZATION
# --------------------------------------------------

@st.cache_resource
def initialize_agent():
    """
    Load the existing vector database and initialize
    the VoyageAI agent only once per application process.
    """

    vector_store = load_vector_store()

    agent = create_voyage_agent(
        vector_store,
        db_path=str(MEMORY_DB)
    )

    return agent


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("✈️ VoyageAI")

    st.caption(
        "Destination Intelligence & Cultural Travel Companion"
    )

    st.divider()

    st.subheader("Destination Guide")

    uploaded_file = st.file_uploader(
        "Upload a destination PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.info(f"Selected: {uploaded_file.name}")

        if st.button(
            "Process and Index PDF",
            use_container_width=True
        ):

            try:
                pdf_path = DATA_DIR / uploaded_file.name

                with open(pdf_path, "wb") as file:
                    file.write(uploaded_file.getbuffer())

                with st.spinner("Reading and processing PDF..."):

                    chunks = load_and_split_pdf(
                        str(pdf_path)
                    )

                    create_vector_store(chunks)

                # Reinitialize agent with the new vector database
                initialize_agent.clear()

                st.success(
                    f"Successfully indexed {len(chunks)} document chunks!"
                )

                st.rerun()

            except Exception as error:
                st.error(f"PDF processing failed: {error}")

    st.divider()

    st.subheader("Available Features")

    st.markdown(
        """
        - 📚 PDF-based question answering
        - 📄 Page-level source citations
        - 💱 Currency conversion
        - 💰 Travel budget estimation
        - 🧠 Conversational memory
        """
    )

    st.divider()

    if st.button(
        "Clear Chat",
        use_container_width=True
    ):
        st.session_state.chat_history = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.caption("Powered by LangChain, Groq, Hugging Face and ChromaDB.")


# --------------------------------------------------
# MAIN INTERFACE
# --------------------------------------------------

st.title("✈️ VoyageAI")
st.subheader("Your Intelligent Japan Travel Companion")

st.write(
    "Explore Japan with an AI assistant that answers questions "
    "using your destination guide, converts currencies, and "
    "estimates travel budgets."
)

st.divider()


# --------------------------------------------------
# LOAD AGENT
# --------------------------------------------------

try:
    agent = initialize_agent()

except Exception as error:

    st.warning(
        "VoyageAI is not ready yet. Please check that a PDF has "
        "been indexed and your Groq API key is configured."
    )

    st.error(str(error))

    st.stop()


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# CHAT INPUT AND AGENT RESPONSE
# --------------------------------------------------

user_query = st.chat_input(
    "Ask VoyageAI about Japan, currency, or travel budgets..."
)

if user_query:

    # Display user message
    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    # Invoke the agent
    with st.chat_message("assistant"):

        with st.spinner("VoyageAI is thinking..."):

            try:

                response = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": user_query
                            }
                        ]
                    },
                    config={
                        "configurable": {
                            "thread_id": st.session_state.thread_id
                        }
                    }
                )

                answer = response["messages"][-1].content

                if not isinstance(answer, str):
                    answer = str(answer)

                st.markdown(answer)

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as error:

                st.error(
                    f"An error occurred while generating the answer: {error}"
                )
