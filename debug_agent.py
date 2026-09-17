import agent
from groq import Groq
import json

def run_debug():
    client = Groq()
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_commitments",
                "description": "Get commitments from the database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "counterparty": {"type": ["string", "null"]},
                        "direction": {"type": ["string", "null"]}
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_source_text",
                "description": "Get the exact transcript text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source_id": {"type": "string"}
                    },
                    "required": ["source_id"]
                }
            }
        }
    ]
    
    messages = [{"role": "system", "content": "You are an executive assistant for Arjun Malhotra. Today is Wednesday, 23 September 2026. Answer questions based ONLY on the tools provided."}]
    messages.append({"role": "user", "content": "Show me exactly what Neha said about the Q3 deck review."})
    
    for _ in range(6):
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=2000
        )
        msg = response.choices[0].message
        print(f"Assistant content: {msg.content}")
        if msg.tool_calls:
            messages.append(msg)
            for t in msg.tool_calls:
                print(f"Tool Call: {t.function.name}({t.function.arguments})")
                if t.function.name == "get_commitments":
                    args = json.loads(t.function.arguments)
                    res = agent.get_commitments(args.get("counterparty"), args.get("direction"))
                    messages.append({"role": "tool", "tool_call_id": t.id, "name": t.function.name, "content": res})
                    print("Tool Returned:", res)
                elif t.function.name == "get_source_text":
                    args = json.loads(t.function.arguments)
                    res = agent.get_source_text(args.get("source_id"))
                    messages.append({"role": "tool", "tool_call_id": t.id, "name": t.function.name, "content": res})
                    print("Tool Returned:", res)
        else:
            break

run_debug()
