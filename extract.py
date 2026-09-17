import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from groq import Groq
import instructor

load_dotenv()

# Initialize the Groq client and wrap it with instructor
client = Groq()
client = instructor.from_groq(client, mode=instructor.Mode.JSON)

class CommitmentCandidate(BaseModel):
    raw_text: str = Field(description="The exact snippet of text that contains the commitment")
    source_ids: list[str] = Field(description="List of source IDs that mention this commitment")
    actor: str = Field(description="The person who must perform the action. Use 'unowned' if not clear or just guessed.")
    counterparty: str = Field(description="The person who receives the action or is waiting on it. Can be 'All' or empty.")
    action: str = Field(description="A short summary of the action to be taken")
    direction: str = Field(description="Must be 'my_action' if Arjun is the actor, otherwise 'waiting_on_other'")
    stated_deadline: str = Field(description="The deadline exactly as stated in this source (e.g., 'Wednesday evening')")
    ownership_clear: bool = Field(description="True if an owner is explicitly stated or accepted. False if it's just a guess (like Divya guessing Facilities).")
    timestamp: str = Field(description="The timestamp of the source message")

class ExtractionResult(BaseModel):
    candidates: list[CommitmentCandidate] = Field(description="List of extracted commitment candidates")

def extract_commitments():
    with open("sources.json", "r") as f:
        sources = json.load(f)
    
    sources_text = json.dumps(sources, indent=2)
    
    prompt = f"""
    You are an AI assistant analyzing a dataset of emails, transcripts, and voice notes for Arjun Malhotra (VP Sales).
    Extract all commitment candidates from the following data.
    
    CRITICAL INSTRUCTIONS:
    1. If a source doesn't explicitly name an owner, DO NOT infer one from their role (e.g. if someone says "I think that's supposed to be Facilities", that means ownership is NOT clear, so set ownership_clear to false and actor to "unowned").
    2. Extract each commitment as accurately as possible. If the same commitment is discussed across multiple sources in a thread, you can extract multiple candidates or one candidate with multiple source_ids.
    3. The direction must be 'my_action' if Arjun is the actor, and 'waiting_on_other' if anyone else is the actor.
    
    Data:
    {sources_text}
    """

    print("Calling Groq API (openai/gpt-oss-120b)...")
    result: ExtractionResult = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        response_model=ExtractionResult,
        max_tokens=8000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    candidates_dict = [c.model_dump() for c in result.candidates]
    
    with open("commitment_candidates.json", "w") as f:
        json.dump(candidates_dict, f, indent=2)
    
    print(f"Extracted {len(candidates_dict)} candidates to commitment_candidates.json")

if __name__ == "__main__":
    extract_commitments()
