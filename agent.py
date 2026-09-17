import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_commitments(counterparty=None, direction=None):
    try:
        with open("commitments.json", "r") as f:
            commitments = json.load(f)
    except FileNotFoundError:
        return "[]"
    
    results = []
    for c in commitments:
        if counterparty:
            c_lower = counterparty.lower()
            actor = c.get("actor", "").lower()
            cparty = c.get("counterparty", "").lower()
            if c_lower not in actor and c_lower not in cparty:
                continue
        if direction and c.get("direction") != direction:
            continue
        results.append(c)
    return json.dumps(results)

def get_source_text(source_id):
    try:
        with open("sources.json", "r") as f:
            sources = json.load(f)
    except FileNotFoundError:
        return "Source not found."
        
    for s in sources:
        if s.get("id") == source_id:
            return json.dumps(s)
    return "Source not found."

def run_agent_turn(user_message, chat_history, as_of_date_str):
    client = Groq()
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_commitments",
                "description": "Get commitments from the database. Use this to find out what was promised, who owes what, and deadlines.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "counterparty": {"type": ["string", "null"], "description": "The person Arjun is interacting with (e.g., raghav, neha, divya)."},
                        "direction": {"type": ["string", "null"], "description": "Either 'my_action' (if Arjun owes it) or 'waiting_on_other' (if someone else owes it to Arjun)."}
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_source_text",
                "description": "Get the exact transcript, email, or voice note text by source_id. Use this when you need exact quotes.",
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
    
    system_prompt = f"You are an executive assistant for Arjun Malhotra. Today is {as_of_date_str}. Answer questions based ONLY on the tools provided. When answering, cite the source_ids."
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
        
    messages.append({"role": "user", "content": user_message})
    
    for _ in range(6):  # Allow up to 6 tool iterations
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=2000
            )
        except Exception as e:
            return f"Agent API Error: {str(e)}"
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        if not tool_calls:
            # If no tools were called, the model is providing the final answer
            return response_message.content or "I'm not sure how to answer that."
            
        messages.append(response_message)
        for tool_call in tool_calls:
            print(f"🤖 [Agent] Calling Tool: {tool_call.function.name} with args {tool_call.function.arguments}")
            if tool_call.function.name == "get_commitments":
                try:
                    args = json.loads(tool_call.function.arguments)
                except:
                    args = {}
                result = get_commitments(args.get("counterparty"), args.get("direction"))
                print(f"📄 [Tool Result] Found {len(json.loads(result))} commitments")
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "name": tool_call.function.name, "content": result})
                
            elif tool_call.function.name == "get_source_text":
                try:
                    args = json.loads(tool_call.function.arguments)
                except:
                    args = {}
                result = get_source_text(args.get("source_id"))
                print(f"📄 [Tool Result] Fetched source: {args.get('source_id')}")
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "name": tool_call.function.name, "content": result})
                
    return "I needed too many steps to answer this. Please try rephrasing."
