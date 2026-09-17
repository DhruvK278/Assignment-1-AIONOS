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
        if counterparty and c.get("counterparty", "").lower() != counterparty.lower():
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
                        "counterparty": {"type": "string", "description": "The person Arjun is interacting with (e.g., raghav, neha, divya)."},
                        "direction": {"type": "string", "description": "Either 'my_action' (if Arjun owes it) or 'waiting_on_other' (if someone else owes it to Arjun)."}
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
    
    # We use a standard try-except in case the model doesn't support tools perfectly
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
    
    if tool_calls:
        # The assistant called a tool
        messages.append(response_message)
        for tool_call in tool_calls:
            if tool_call.function.name == "get_commitments":
                try:
                    args = json.loads(tool_call.function.arguments)
                except:
                    args = {}
                result = get_commitments(args.get("counterparty"), args.get("direction"))
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "name": tool_call.function.name, "content": result})
                
            elif tool_call.function.name == "get_source_text":
                try:
                    args = json.loads(tool_call.function.arguments)
                except:
                    args = {}
                result = get_source_text(args.get("source_id"))
                messages.append({"role": "tool", "tool_call_id": tool_call.id, "name": tool_call.function.name, "content": result})
                
        # Send tool results back to the model
        try:
            final_response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                max_tokens=2000
            )
            return final_response.choices[0].message.content
        except Exception as e:
            return f"Agent API Error during tool resolution: {str(e)}"
            
    # If no tools were called
    return response_message.content or "I'm not sure how to answer that."
