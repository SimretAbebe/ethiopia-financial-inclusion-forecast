from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"

UNIFIED_DATA_FILE = DATA_RAW_DIR / "ethiopia_fi_unified_data.xlsx"
REFERENCE_CODES_FILE = DATA_RAW_DIR / "reference_codes.xlsx"

SHEET_MAIN = "ethiopia_fi_unified_data"
SHEET_IMPACT = "Impact_sheet"

RECORD_TYPES = ["observation", "event", "impact_link", "target", "baseline", "forecast"]
PILLARS = ["ACCESS", "USAGE", "QUALITY", "AFFORDABILITY", "TRUST", "DEPTH", "GENDER"]
CONFIDENCE_LEVELS = ["high", "medium", "low", "estimated"]
EVENT_CATEGORIES = [
    "product_launch", "market_entry", "market_exit", "policy",
    "regulation", "infrastructure", "partnership", "milestone",
    "economic", "pricing",
]