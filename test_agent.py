
from modules.vector_store import load_vector_store
from modules.agent import create_voyage_agent


print("Loading VoyageAI...")

vector_store = load_vector_store()

agent = create_voyage_agent(
    vector_store,
    db_path="voyage_memory.db"
)

config = {
    "configurable": {
        "thread_id": "voyage_tool_verification"
    }
}


def ask_voyageai(question):

    print("\n" + "=" * 60)
    print("QUESTION:", question)

    # Get the existing conversation length
    previous_state = agent.get_state(config)
    previous_messages = previous_state.values.get("messages", [])
    previous_count = len(previous_messages)

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config=config
    )

    print("\nVOYAGEAI RESPONSE:")
    print(response["messages"][-1].content)

    # Inspect only messages generated during this question
    current_messages = response["messages"][previous_count:]

    tool_calls = [
        message.name
        for message in current_messages
        if getattr(message, "type", "") == "tool"
    ]

    print("\nTOOLS USED:", tool_calls or "No tools called")


ask_voyageai(
    "According to the Japan guide, what is the police emergency number?"
)

ask_voyageai(
    "Convert 100 USD into Japanese Yen."
)

ask_voyageai(
    "Estimate my Japan travel budget for 7 days using the moderate travel style."
)

ask_voyageai(
    "Which country and currency were we discussing earlier?"
)

ask_voyageai(
    "What will the exact weather be in Tokyo on December 15, 2026?"
)

print("\nAGENT VERIFICATION COMPLETED!")
