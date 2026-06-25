import requests
import re

COMPANIES_FILE = "test-vendors.txt"
API_URL = "https://api.ransomware.live/v2/recentvictims"

NOISE_WORDS = {
    "llc", "inc", "ltd", "corp", "corporation", "co",
    "group", "solutions", "services", "service",
    "company", "plc", "holdings", "technologies", "tech",
    "international", "global"
}

LOW_VALUE_TOKENS = {
    "smith", "johnson", "brown", "wilson", "lee", "taylor",
    "and", "the", "of", "for"
}

GENERIC_TOKENS = {
    "global",
    "systems",
    "solutions",
    "technology",
    "technologies",
    "services",
    "consulting",
    "software",
    "medical",
    "health",
    "digital",
    "energy"
}


def load_companies(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]


def fetch_recent_victims():
    r = requests.get(API_URL, timeout=30)
    r.raise_for_status()
    return r.json()


def extract_victim_name(victim: dict) -> str:
    return (
        victim.get("name")
        or victim.get("victim")
        or victim.get("title")
        or ""
    ).strip()


def is_masked_name(name: str) -> bool:
    """
    Detect partial/redacted victim names like:
    G*
    H**
    Acm*
    Micros***
    """
    name = name.strip()

    patterns = [
        r"[A-Za-z]\*+",     # G*
        r"[A-Za-z]{2,}\*+", # Acm*
        r".+\*+$"          # anything ending in ***
    ]

    return any(re.fullmatch(p, name) for p in patterns)


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return text


def build_tokens(name: str):
    name = normalize(name)
    return [
        t for t in name.split()
        if t not in NOISE_WORDS and t not in LOW_VALUE_TOKENS
    ]


def is_high_value_single_token(token: str) -> bool:
    """
    Only allow single-token matching if the token is distinctive enough.
    """
    return (
        len(token) >= 7
        and token not in GENERIC_TOKENS
    )


def match(vendor: str, victim: str) -> bool:
    v_tokens = build_tokens(vendor)
    k_tokens = build_tokens(victim)

    if not v_tokens or not k_tokens:
        return False

    v_set = set(v_tokens)
    k_set = set(k_tokens)

    # CASE 1: exact match
    if v_set == k_set:
        return True

    # CASE 2: subset match (multi-token entities only)
    if len(v_set) >= 2 and (v_set.issubset(k_set) or k_set.issubset(v_set)):
        return True

    # CASE 3: single-token overlap (strict)
    if len(v_set) == 1 or len(k_set) == 1:
        common = list(v_set & k_set)

        if not common:
            return False

        token = common[0]

        if is_high_value_single_token(token):
            return True

        return False

    # CASE 4: partial overlap scoring
    overlap = len(v_set & k_set)
    score = overlap / max(len(v_set), len(k_set))

    return score >= 0.6


def match_companies(companies, victims):
    for company in companies:

        for victim in victims:

            victim_name = extract_victim_name(victim)

            # 🔥 FIX: skip masked / invalid names early
            if not victim_name or is_masked_name(victim_name):
                continue

            if match(company, victim_name):

                print("⚠️ MATCH FOUND")
                print(f"Vendor : {company}")
                print(f"Victim : {victim_name}")
                print(f"Group  : {victim.get('group','')}")
                print(f"Domain : {victim.get('domain','')}")
                print(f"Date   : {victim.get('attackdate','')}")
                print("-" * 50)


def main():
    companies = load_companies(COMPANIES_FILE)
    victims = fetch_recent_victims()
    match_companies(companies, victims)


if __name__ == "__main__":
    main()
