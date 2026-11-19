
import os
import sqlite3
from pathlib import Path
from langchain.tools import tool
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver


from modules.tools import get_voyage_tools


load_dotenv()


def create_voyage_agent(vector_store, db_path="voyage_memory.db"):
    """
    Create the VoyageAI agent with:
    1. Japan PDF retrieval
    2. Currency conversion
    3. Travel budget estimation
    4. Persistent SQLite conversation memory
    """

    # Check Groq API key
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to your .env file."
        )

    # Configure the Groq language model
    model_name = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b"
    )

    llm = ChatGroq(
        model=model_name,
        temperature=0.1,
        api_key=api_key
    )

    # Create the PDF retrieval tool
    @tool
    def search_japan_guide(query: str) -> str:
        """
        Search the uploaded Japan destination guide.

        Use this tool for questions about Japanese destinations,
        transport, landmarks, customs, food, safety, seasons,
        accommodation, currency information, and visa guidance.

        Returns relevant passages with their original PDF page numbers.
        """

        documents = vector_store.similarity_search(
            query,
            k=4
        )

        if not documents:
            return "No relevant information was found in the Japan guide."

        results = []

        for document in documents:
            page_number = document.metadata.get(
                "page_number",
                "Unknown"
            )

            results.append(
                f"[Source: Japan Destination Guide, Page {page_number}]\n"
                f"{document.page_content}"
            )

        return "\n\n".join(results)

    # Register all three tools
    tools = [
        search_japan_guide,
        *get_voyage_tools()
    ]

    # Agent instructions
    system_prompt = """
You are VoyageAI, a Smart Travel Guide and Itinerary Assistant
specialized in Japan, particularly Tokyo and Kyoto.

YOUR RESPONSIBILITIES:

1. DOCUMENT-BASED QUESTIONS
For questions about Japan, Tokyo, Kyoto, transportation,
landmarks, local customs, food, safety, seasons, accommodation,
currency information, and visa guidance:

- Always use the search_japan_guide tool first.
- Base your answer on the retrieved document passages.
- Include the exact page number(s) supplied by the retrieval tool.
- Use citations such as [Source: Japan Destination Guide, Page 4].
- Never invent facts, page numbers, or document citations.
- If the document does not contain the requested information,
  clearly say that it is not available in the provided guide.

2. CURRENCY CONVERSION
Use convert_currency when a user requests a currency conversion.
Explain that its rates are illustrative reference rates, not live rates.

3. TRAVEL BUDGET ESTIMATION
Use estimate_travel_budget when a user requests a travel budget.
Explain what the estimate includes and excludes.

4. CONVERSATION
- Remember relevant information from previous messages.
- Understand follow-up questions using conversation history.
- Be clear, practical, and concise.
- Do not claim that a tool was used if it was not.

5. ITINERARY QUESTIONS
Use the destination guide for available destination information.
Do not invent document-based facts or present unsupported details
as facts from the guide.

If a question is unrelated to the guide or travel tools,
politely explain your specialization.
"""

    # Create persistent SQLite checkpoint storage
    database_path = Path(db_path).resolve()
    database_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        str(database_path),
        check_same_thread=False
    )

    checkpointer = SqliteSaver(connection)

    # Build the LangChain v1 agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer,
        name="voyageai_agent"
    )

    return agent
