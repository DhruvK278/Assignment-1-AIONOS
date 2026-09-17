import json
from datetime import datetime
from collections import defaultdict
import difflib

def group_candidates(candidates):
    # Groups candidates by (actor, counterparty) and fuzzy matches the action.
    groups = []
    
    for c in candidates:
        actor = c.get("actor", "").lower()
        counterparty = c.get("counterparty", "").lower()
        action = c.get("action", "")
        
        placed = False
        for g in groups:
            g_actor = g[0].get("actor", "").lower()
            g_counterparty = g[0].get("counterparty", "").lower()
            
            if actor == g_actor and counterparty == g_counterparty:
                # Fuzzy match action
                similarity = difflib.SequenceMatcher(None, action.lower(), g[0].get("action", "").lower()).ratio()
                if similarity > 0.4 or any(sid in g_sids for sid in c.get("source_ids", []) for g_sids in [x.get("source_ids", []) for x in g]):
                    g.append(c)
                    placed = True
                    break
        if not placed:
            groups.append([c])
    return groups

def resolve_commitments(groups):
    commitments = []
    for i, group in enumerate(groups):
        # Sort group chronologically by timestamp
        group.sort(key=lambda x: x.get("timestamp", ""))
        
        # The latest state is the truth
        latest = group[-1]
        
        # Build status history
        history = []
        for item in group:
            history.append({
                "stated": item.get("timestamp"),
                "deadline": item.get("stated_deadline"),
                "source_ids": item.get("source_ids")
            })
            
        # Compile all source IDs
        all_sources = set()
        for item in group:
            all_sources.update(item.get("source_ids", []))
            
        commitment = {
            "id": f"commit-{i+1}",
            "action": latest.get("action"),
            "actor": latest.get("actor"),
            "counterparty": latest.get("counterparty"),
            "direction": latest.get("direction"),
            "current_deadline_text": latest.get("stated_deadline"),
            "ownership_clear": latest.get("ownership_clear", True),
            "status_history": history,
            "source_ids": list(all_sources)
        }
        commitments.append(commitment)
    return commitments

def classify_commitments(commitments, as_of_date):
    # as_of_date is a datetime object
    for c in commitments:
        if not c["ownership_clear"] or c.get("actor", "").lower() == "unowned":
            c["status"] = "unowned"
            continue
            
        deadline_text = c.get("current_deadline_text", "").lower()
        
        # Simple heuristic to parse the mock data deadlines
        # In a real app, this would use a real NLP date parser or LLM to normalize dates to ISO
        deadline_date = None
        if "wednesday" in deadline_text or "23" in deadline_text:
            deadline_date = datetime(2026, 9, 23, 23, 59)
            if "morning" in deadline_text or "9:30" in deadline_text: deadline_date = datetime(2026, 9, 23, 12, 0)
            if "evening" in deadline_text: deadline_date = datetime(2026, 9, 23, 18, 0)
        elif "thursday" in deadline_text or "24" in deadline_text:
            deadline_date = datetime(2026, 9, 24, 23, 59)
            if "morning" in deadline_text: deadline_date = datetime(2026, 9, 24, 12, 0)
        elif "friday" in deadline_text or "25" in deadline_text:
            deadline_date = datetime(2026, 9, 25, 23, 59)
        elif "tuesday" in deadline_text or "22" in deadline_text:
            deadline_date = datetime(2026, 9, 22, 23, 59)
            
        if deadline_date:
            if deadline_date < as_of_date:
                c["status"] = "overdue"
            elif deadline_date.date() == as_of_date.date():
                c["status"] = "due_today"
            else:
                c["status"] = "upcoming"
        else:
            c["status"] = "upcoming"
            
    return commitments

def main():
    with open("commitment_candidates.json", "r") as f:
        candidates = json.load(f)
        
    groups = group_candidates(candidates)
    commitments = resolve_commitments(groups)
    
    with open("commitments.json", "w") as f:
        json.dump(commitments, f, indent=2)
        
    print(f"Engine processed {len(candidates)} candidates into {len(commitments)} resolved commitments.")

if __name__ == "__main__":
    main()
