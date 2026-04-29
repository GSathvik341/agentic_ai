import os
from dotenv import load_dotenv

load_dotenv()   # Load .env FIRST

from tools.agent import run_agent


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Missing OPENAI_API_KEY in .env")
        return

    print("Agentic AI Assistant Ready")
    print("Type exit to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break

        answer = run_agent(user_input)
        print("\nAssistant:", answer, "\n")


if __name__ == "__main__":
    main()