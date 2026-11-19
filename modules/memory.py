import os
from langchain_community.chat_message_histories import SQLChatMessageHistory

DB_PATH = "sqlite.db"

def get_session_history(session_id: str) -> SQLChatMessageHistory:
    """
    Returns an instance of SQLChatMessageHistory for a given unique session ID.
    This stores conversation history in a local SQLite database.
    """
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=f"sqlite:///{DB_PATH}"
    )

def clear_session_history(session_id: str):
    """
    Clears the chat history for a specific session ID.
    """
    history = get_session_history(session_id)
    history.clear()