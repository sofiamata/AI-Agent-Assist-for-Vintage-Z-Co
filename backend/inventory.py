import json
from pathlib import Path
from typing import List, Dict, Any

# Load inventory from JSON file
json_path = Path(__file__).parent.parent / "inventory.JSON"
with open(json_path, 'r') as f:
    INVENTORY: List[Dict[str, Any]] = json.load(f)

def search_inventory(query: str) -> List[Dict[str, Any]]:
    q = query.lower()
    hits = []
    for item in INVENTORY:
        blob = f"{item['part']} {item['model']} {item.get('side') or ''}".lower()
        if any(tok in blob for tok in q.split()):
            hits.append(item)
    return hits[:5]
