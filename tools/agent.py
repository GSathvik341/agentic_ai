import os
import json
from openai import OpenAI
from tools.weather import get_current_weather
from tools.rag import search_polity_document

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are a helpful AI assistant.

You have two tools:

1. get_current_weather(city)
Use for weather questions.

2. search_polity_document(query)
Use for Indian Polity / Constitution / Parliament / President / Judiciary questions.

Rules:
- Use tools whenever relevant.
- If no tool applies, answer politely that you only support weather and Indian polity.
- Use concise professional answers.
"""


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_polity_document",
            "description": "Search Indian polity knowledge base",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]


def run_agent(user_input: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        tools=TOOLS,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    if not msg.tool_calls:
        return msg.content

    tool_outputs = []

    for call in msg.tool_calls:
        fn_name = call.function.name
        args = json.loads(call.function.arguments)

        if fn_name == "get_current_weather":
            result = get_current_weather(args["city"])

        elif fn_name == "search_polity_document":
            result = search_polity_document(args["query"])

        else:
            result = "Unknown tool."

        tool_outputs.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": str(result)
        })

    second_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
            msg,
            *tool_outputs
        ]
    )

    return second_response.choices[0].message.content
