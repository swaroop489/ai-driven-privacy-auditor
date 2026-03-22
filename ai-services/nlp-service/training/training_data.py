"""
training_data.py
----------------
Synthetic training data generator for Indian PII NER model.

Generates annotated training examples in spaCy NER format:
    (text, {"entities": [(start, end, label)]})

Entity types:
    - AADHAR: 12-digit Indian Unique Identification number
    - PAN: Permanent Account Number (10 chars, e.g., ABCDE1234F)
    - INDIAN_PHONE: Indian mobile numbers (+91 / 0 prefixed)
    - EMAIL: Email addresses
    - UPI_ID: Unified Payments Interface ID (e.g., name@upi)
    - VOTER_ID: Indian Voter ID (e.g., ABC1234567)
    - PASSPORT_IN: Indian Passport Number (e.g., A1234567)
    - IFSC: Indian Financial System Code (e.g., SBIN0001234)
    - DL_NUMBER: Driving License Number (e.g., MH-01-2020-0012345)

All data is SYNTHETIC — no real PII is used.
"""

import random
import json
from typing import List, Tuple, Dict

# ============================================================
# Seed data pools — all FAKE / synthetic
# ============================================================

FIRST_NAMES = [
    "Rahul", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rohit", "Neha",
    "Suresh", "Deepika", "Karthik", "Pooja", "Arjun", "Divya", "Manish",
    "Kavita", "Rajesh", "Shalini", "Abhishek", "Meera", "Sanjay", "Lakshmi",
    "Varun", "Ananya", "Gaurav", "Ritika", "Prakash", "Sunita", "Nikhil",
    "Swati", "Aakash", "Bhavna", "Dinesh", "Geeta", "Harish", "Jaya"
]

LAST_NAMES = [
    "Sharma", "Patel", "Kumar", "Singh", "Verma", "Gupta", "Reddy",
    "Nair", "Iyer", "Joshi", "Desai", "Mehta", "Chopra", "Malhotra",
    "Pillai", "Rao", "Das", "Bhat", "Kulkarni", "Agarwal", "Mishra",
    "Tiwari", "Pandey", "Saxena", "Kapoor", "Trivedi", "Banerjee"
]

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Pune",
    "Chennai", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow",
    "Indore", "Nagpur", "Coimbatore", "Patna", "Bhopal",
    "Kochi", "Chandigarh", "Visakhapatnam", "Surat", "Thiruvananthapuram"
]

STATES = [
    "Maharashtra", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "Gujarat",
    "Rajasthan", "Kerala", "Telangana", "West Bengal", "Madhya Pradesh"
]

STATE_CODES = [
    "MH", "KA", "TN", "UP", "GJ", "RJ", "KL", "TS", "WB", "MP",
    "DL", "HR", "PB", "AP", "BR", "GA", "JH", "OR", "CG", "AS"
]

UPI_HANDLES = [
    "paytm", "ybl", "oksbi", "okhdfcbank", "okicici", "apl",
    "ibl", "axl", "upi", "freecharge", "gpay", "phonepe"
]

BANK_CODES = [
    "SBIN", "HDFC", "ICIC", "PUNB", "BARB", "CNRB", "UBIN",
    "IOBA", "BKID", "CORP", "MAHB", "KKBK", "UTIB", "IDIB"
]

EMAIL_DOMAINS = [
    "gmail.com", "yahoo.co.in", "outlook.com", "hotmail.com",
    "rediffmail.com", "protonmail.com", "ymail.com", "icloud.com"
]

PAN_FOURTH_CHARS = {
    "P": "Individual", "C": "Company", "H": "HUF",
    "F": "Firm", "A": "AOP", "T": "Trust"
}

# ============================================================
# Generators for each PII type
# ============================================================

def gen_aadhar() -> str:
    """Generate a fake Aadhar number: XXXX XXXX XXXX"""
    digits = [str(random.randint(0, 9)) for _ in range(12)]
    # Aadhar doesn't start with 0 or 1
    digits[0] = str(random.randint(2, 9))
    return f"{''.join(digits[:4])} {''.join(digits[4:8])} {''.join(digits[8:12])}"


def gen_aadhar_nospace() -> str:
    """Generate fake Aadhar without spaces: XXXXXXXXXXXX"""
    digits = [str(random.randint(0, 9)) for _ in range(12)]
    digits[0] = str(random.randint(2, 9))
    return ''.join(digits)


def gen_pan() -> str:
    """Generate a fake PAN: ABCDE1234F"""
    c1 = chr(random.randint(65, 90))
    c2 = chr(random.randint(65, 90))
    c3 = chr(random.randint(65, 90))
    c4 = random.choice(list(PAN_FOURTH_CHARS.keys()))
    c5 = chr(random.randint(65, 90))
    digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    c6 = chr(random.randint(65, 90))
    return f"{c1}{c2}{c3}{c4}{c5}{digits}{c6}"


def gen_phone() -> str:
    """Generate a fake Indian phone number"""
    formats = [
        lambda: f"+91 {random.randint(6,9)}{random.randint(100000000, 999999999):09d}",
        lambda: f"+91-{random.randint(6,9)}{random.randint(100000000, 999999999):09d}",
        lambda: f"0{random.randint(6,9)}{random.randint(100000000, 999999999):09d}",
        lambda: f"{random.randint(6,9)}{random.randint(100000000, 999999999):09d}",
        lambda: f"+91 {random.randint(6,9)}{random.randint(100, 999):03d} {random.randint(100, 999):03d} {random.randint(1000, 9999):04d}",
    ]
    return random.choice(formats)()


def gen_email() -> str:
    """Generate a fake email address"""
    first = random.choice(FIRST_NAMES).lower()
    last = random.choice(LAST_NAMES).lower()
    domain = random.choice(EMAIL_DOMAINS)
    sep = random.choice([".", "_", ""])
    num = random.choice(["", str(random.randint(1, 999))])
    return f"{first}{sep}{last}{num}@{domain}"


def gen_upi() -> str:
    """Generate a fake UPI ID"""
    first = random.choice(FIRST_NAMES).lower()
    last = random.choice(LAST_NAMES).lower()
    handle = random.choice(UPI_HANDLES)
    sep = random.choice([".", "_", ""])
    num = random.choice(["", str(random.randint(1, 99))])
    return f"{first}{sep}{last}{num}@{handle}"


def gen_voter_id() -> str:
    """Generate a fake Voter ID: ABC1234567"""
    letters = ''.join([chr(random.randint(65, 90)) for _ in range(3)])
    digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"{letters}{digits}"


def gen_passport() -> str:
    """Generate a fake Indian Passport Number: A1234567"""
    letter = chr(random.randint(65, 90))
    digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"{letter}{digits}"


def gen_ifsc() -> str:
    """Generate a fake IFSC code: SBIN0001234"""
    bank = random.choice(BANK_CODES)
    branch = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return f"{bank}0{branch}"


def gen_dl() -> str:
    """Generate a fake Indian Driving License: MH-01-2020-0012345"""
    state = random.choice(STATE_CODES)
    rto = f"{random.randint(1, 50):02d}"
    year = str(random.randint(2005, 2024))
    serial = f"{random.randint(1, 9999999):07d}"
    return f"{state}-{rto}-{year}-{serial}"


# ============================================================
# Sentence templates with {PII} placeholders
# ============================================================

AADHAR_TEMPLATES = [
    "My Aadhar number is {PII}.",
    "Please verify the Aadhar: {PII} for KYC.",
    "Aadhar card details: {PII}, issued to {NAME}.",
    "The customer's Aadhar ID is {PII}.",
    "For UIDAI verification, please use {PII}.",
    "My aadhaar no. is {PII} linked to my mobile.",
    "Submit your Aadhar ({PII}) for identity proof.",
    "Aadhar: {PII}. Please update the records.",
    "He showed his Aadhar card {PII} at the bank counter.",
    "Link your bank account with Aadhar {PII}.",
    "Her Aadhar number {PII} is already registered.",
    "Aadhar enrollment number: {PII}.",
    "Send a copy of your Aadhar card. Number is {PII}.",
    "I need to update my Aadhar details. Current number: {PII}.",
    "The Aadhar {PII} has been successfully verified.",
    "Government ID (Aadhaar): {PII}.",
    "Please enter your 12-digit Aadhar number: {PII}.",
    "eKYC completed with Aadhar {PII}.",
    "My UID number from UIDAI is {PII}.",
    "I lost my Aadhar card, the number was {PII}.",
]

PAN_TEMPLATES = [
    "My PAN card number is {PII}.",
    "PAN: {PII} belongs to {NAME}.",
    "For ITR filing, use PAN {PII}.",
    "The TDS certificate shows PAN {PII}.",
    "PAN number {PII} is linked to my bank account.",
    "Please provide your PAN ({PII}) for tax purposes.",
    "Income Tax PAN: {PII}.",
    "His Permanent Account Number is {PII}.",
    "PAN card details: {PII}, Name: {NAME}.",
    "Enter PAN {PII} to complete the registration.",
    "My father's PAN is {PII}.",
    "Company PAN: {PII}, registered in {CITY}.",
    "For GST registration, PAN {PII} is required.",
    "PAN verification failed for {PII}. Please recheck.",
    "Submit PAN card copy. Number: {PII}.",
    "I received Form 16 with PAN {PII}.",
    "Tax deducted against PAN {PII}.",
    "My PAN is {PII} and I need to link it with Aadhar.",
    "The PAN {PII} is already registered with the IT department.",
    "Permanent Account Number: {PII}.",
]

PHONE_TEMPLATES = [
    "Call me at {PII}.",
    "My phone number is {PII}.",
    "Contact: {PII} for further details.",
    "Reach {NAME} at {PII}.",
    "WhatsApp me on {PII}.",
    "Send OTP to {PII}.",
    "The mobile number registered is {PII}.",
    "For support, dial {PII}.",
    "My contact number: {PII}.",
    "SMS sent to {PII} successfully.",
    "Please call {PII} between 10 AM and 6 PM.",
    "Alternate mobile: {PII}.",
    "The customer's phone number is {PII}.",
    "I can be reached at {PII} anytime.",
    "His registered mobile number is {PII}.",
    "New SIM card activated for {PII}.",
    "Number {PII} has been ported to Jio.",
    "Emergency contact: {PII}.",
    "Phone: {PII}, verified via OTP.",
    "The delivery will be confirmed on {PII}.",
]

EMAIL_TEMPLATES = [
    "Email me at {PII}.",
    "Send the documents to {PII}.",
    "My email address is {PII}.",
    "For queries, write to {PII}.",
    "Contact email: {PII}.",
    "The registered email is {PII}.",
    "Invoice will be sent to {PII}.",
    "Reset password link sent to {PII}.",
    "Email ID: {PII} is verified.",
    "Please update my email to {PII}.",
    "Confirmation mail sent to {PII}.",
    "Official correspondence: {PII}.",
    "My alternate email is {PII}.",
    "Login with {PII} and your password.",
    "Notification preferences set for {PII}.",
]

UPI_TEMPLATES = [
    "Pay me via UPI: {PII}.",
    "My UPI ID is {PII}.",
    "Send money to {PII} on Google Pay.",
    "UPI address: {PII}.",
    "Transfer the amount to UPI {PII}.",
    "My PhonePe ID: {PII}.",
    "Payment received from {PII}.",
    "Scan or use UPI ID {PII} for payment.",
    "Link UPI {PII} with your bank account.",
    "Refund initiated to UPI {PII}.",
    "Please send Rs. 500 to {PII}.",
    "Merchant UPI: {PII}.",
    "Split bill — send your share to {PII}.",
    "My Paytm UPI handle is {PII}.",
    "Vendor payment UPI: {PII}.",
]

VOTER_TEMPLATES = [
    "My Voter ID is {PII}.",
    "Voter ID card number: {PII}.",
    "EPIC number: {PII} for {NAME}.",
    "Election card details: {PII}, {CITY} constituency.",
    "Voter registration number {PII} is active.",
    "Submit Voter ID {PII} as address proof.",
    "The electoral roll shows ID {PII}.",
    "My voter card number is {PII}.",
    "Verified voter: {PII}.",
    "Voter ID {PII} is registered in {STATE}.",
]

PASSPORT_TEMPLATES = [
    "My passport number is {PII}.",
    "Indian passport: {PII}, issued in {CITY}.",
    "Passport No. {PII} expires in 2030.",
    "Travel document: {PII}.",
    "Visa application with passport {PII}.",
    "Passport details — Number: {PII}, Name: {NAME}.",
    "Immigration check: Passport {PII}.",
    "My Indian passport is {PII}.",
    "Passport {PII} issued by RPO {CITY}.",
    "Renewal application for passport {PII}.",
]

IFSC_TEMPLATES = [
    "Bank IFSC code: {PII}.",
    "Transfer via NEFT, IFSC: {PII}.",
    "My bank's IFSC is {PII}.",
    "RTGS payment to IFSC {PII}.",
    "Branch IFSC: {PII}, {CITY}.",
    "For IMPS, use IFSC code {PII}.",
    "Account IFSC: {PII}, Account Name: {NAME}.",
    "The IFSC for {CITY} branch is {PII}.",
    "Bank details — IFSC: {PII}.",
    "Wire transfer IFSC code: {PII}.",
]

DL_TEMPLATES = [
    "My driving license number is {PII}.",
    "DL Number: {PII}, issued by RTO {CITY}.",
    "Driving licence: {PII}, valid till 2030.",
    "License number {PII} for {NAME}.",
    "RTO DL: {PII}.",
    "My DL: {PII}, two-wheeler + four-wheeler.",
    "Driving license details: {PII}.",
    "Suspended DL number: {PII}.",
    "Traffic challan against DL {PII}.",
    "Learner's license upgraded: {PII}.",
]

# ============================================================
# Mixed/multi-PII templates
# ============================================================

MULTI_PII_TEMPLATES = [
    "Name: {NAME}. Aadhar: {AADHAR}. PAN: {PAN}. Phone: {PHONE}.",
    "KYC Form - Name: {NAME}, Aadhar: {AADHAR}, PAN: {PAN}, Email: {EMAIL}.",
    "Please send Rs 1000 to my UPI {UPI}, and call me on {PHONE} once done.",
    "Passport: {PASSPORT}, linked to Aadhar {AADHAR}. Contact: {PHONE}.",
    "Bank account - IFSC: {IFSC}, PAN: {PAN}, UPI: {UPI}.",
    "Employee record: {NAME}, PAN: {PAN}, Phone: {PHONE}, DL: {DL}.",
    "Voter ID: {VOTER}, Aadhar: {AADHAR}, Address: {CITY}, {STATE}.",
    "{NAME}'s profile: Phone {PHONE}, Email {EMAIL}, PAN {PAN}.",
    "Account holder {NAME} with Aadhar {AADHAR} and IFSC {IFSC}.",
    "Verification — Passport {PASSPORT}, PAN {PAN}, Phone {PHONE}.",
]

# ============================================================
# Negative examples (no PII)
# ============================================================

NEGATIVE_EXAMPLES = [
    "The weather in India is very hot during summers.",
    "Cricket is the most popular sport in the country.",
    "I had a great time at the conference yesterday.",
    "The new restaurant on MG Road serves excellent biryani.",
    "Our quarterly targets have been exceeded by 15 percent.",
    "Please submit the project report by end of day Friday.",
    "The train from Mumbai to Delhi takes about 16 hours.",
    "Diwali is celebrated with lights and sweets across India.",
    "The stock market showed positive trends this quarter.",
    "We need to discuss the budget allocation for Q3.",
    "The team meeting is scheduled for Monday at 10 AM.",
    "Bangalore has become the IT capital of India.",
    "The monsoon season brings relief from the summer heat.",
    "Our company has offices in five major Indian cities.",
    "Please review the attached document and provide feedback.",
    "The library has an extensive collection of research papers.",
    "Highway construction between Pune and Mumbai is progressing.",
    "The agriculture sector contributes significantly to GDP.",
    "We had our annual day celebration last week.",
    "Customer satisfaction scores have improved significantly.",
    "The new policy will be effective from next month.",
    "India has a diverse culture with many languages.",
    "The product launch event was attended by over 500 people.",
    "We are looking to expand operations in tier-2 cities.",
    "The internship program starts in June every year.",
    "Our R&D team has filed 3 new patents this year.",
    "The hackathon was won by a team of four engineers.",
    "Food delivery apps have changed dining habits in urban India.",
    "The metro line extension will reduce commute times.",
    "Annual performance reviews will begin next week.",
]


# ============================================================
# Core: Build annotated training example
# ============================================================

def _fill_contextual(template: str) -> Tuple[str, dict]:
    """Fill contextual placeholders like {NAME}, {CITY}, {STATE}"""
    replacements = {}
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    city = random.choice(CITIES)
    state = random.choice(STATES)

    result = template
    result = result.replace("{NAME}", name)
    result = result.replace("{CITY}", city)
    result = result.replace("{STATE}", state)

    return result


def _create_single_entity_example(
    template: str, pii_value: str, label: str
) -> Tuple[str, Dict]:
    """
    Create a spaCy training example from a template with one {PII} placeholder.
    Returns: (text, {"entities": [(start, end, label)]})
    """
    filled = _fill_contextual(template)
    start = filled.index("{PII}")
    end = start + len(pii_value)
    text = filled.replace("{PII}", pii_value)
    return (text, {"entities": [(start, end, label)]})


def _create_multi_entity_example(template: str) -> Tuple[str, Dict]:
    """
    Create a spaCy training example from a multi-PII template.
    Returns: (text, {"entities": [(start, end, label), ...]})
    """
    text = _fill_contextual(template)
    entities = []

    # Generate and replace each PII type
    pii_map = {
        "{AADHAR}": (gen_aadhar, "AADHAR"),
        "{PAN}": (gen_pan, "PAN"),
        "{PHONE}": (gen_phone, "INDIAN_PHONE"),
        "{EMAIL}": (gen_email, "EMAIL"),
        "{UPI}": (gen_upi, "UPI_ID"),
        "{VOTER}": (gen_voter_id, "VOTER_ID"),
        "{PASSPORT}": (gen_passport, "PASSPORT_IN"),
        "{IFSC}": (gen_ifsc, "IFSC"),
        "{DL}": (gen_dl, "DL_NUMBER"),
    }

    for placeholder, (generator, label) in pii_map.items():
        while placeholder in text:
            value = generator()
            start = text.index(placeholder)
            end = start + len(value)
            text = text.replace(placeholder, value, 1)
            entities.append((start, end, label))

    return (text, {"entities": entities})


# ============================================================
# Main: Generate full training dataset
# ============================================================

def generate_training_data(
    examples_per_type: int = 20,
    include_negatives: bool = True,
    include_multi: bool = True,
    seed: int = 42
) -> List[Tuple[str, Dict]]:
    """
    Generate the complete annotated training dataset.

    Args:
        examples_per_type: Number of examples per PII type
        include_negatives: Whether to include negative (no-PII) examples
        include_multi: Whether to include multi-entity examples
        seed: Random seed for reproducibility

    Returns:
        List of (text, annotations) tuples in spaCy format
    """
    random.seed(seed)

    data = []

    # Single-entity examples
    type_configs = [
        (AADHAR_TEMPLATES, gen_aadhar, "AADHAR"),
        (AADHAR_TEMPLATES[:5], gen_aadhar_nospace, "AADHAR"),
        (PAN_TEMPLATES, gen_pan, "PAN"),
        (PHONE_TEMPLATES, gen_phone, "INDIAN_PHONE"),
        (EMAIL_TEMPLATES, gen_email, "EMAIL"),
        (UPI_TEMPLATES, gen_upi, "UPI_ID"),
        (VOTER_TEMPLATES, gen_voter_id, "VOTER_ID"),
        (PASSPORT_TEMPLATES, gen_passport, "PASSPORT_IN"),
        (IFSC_TEMPLATES, gen_ifsc, "IFSC"),
        (DL_TEMPLATES, gen_dl, "DL_NUMBER"),
    ]

    for templates, generator, label in type_configs:
        for i in range(examples_per_type):
            template = templates[i % len(templates)]
            pii_value = generator()
            example = _create_single_entity_example(template, pii_value, label)
            data.append(example)

    # Multi-entity examples
    if include_multi:
        for template in MULTI_PII_TEMPLATES:
            for _ in range(3):  # 3 variations each
                example = _create_multi_entity_example(template)
                data.append(example)

    # Negative examples (no entities)
    if include_negatives:
        for text in NEGATIVE_EXAMPLES:
            data.append((text, {"entities": []}))

    random.shuffle(data)
    return data


def save_training_data(filepath: str, data: List[Tuple[str, Dict]]):
    """Save training data to JSON file"""
    serializable = [(text, ann) for text, ann in data]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} training examples to {filepath}")


def load_training_data(filepath: str) -> List[Tuple[str, Dict]]:
    """Load training data from JSON file"""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)
    data = [(text, {"entities": [tuple(e) for e in ann["entities"]]}) for text, ann in raw]
    return data


# ============================================================
# CLI Entry Point
# ============================================================

if __name__ == "__main__":
    print("Generating synthetic Indian PII training data...")

    data = generate_training_data(examples_per_type=20, seed=42)

    # Stats
    entity_counts = {}
    for _, ann in data:
        for _, _, label in ann["entities"]:
            entity_counts[label] = entity_counts.get(label, 0) + 1

    print(f"\nTotal examples: {len(data)}")
    print(f"Negative examples: {sum(1 for _, a in data if not a['entities'])}")
    print(f"\nEntity distribution:")
    for label, count in sorted(entity_counts.items()):
        print(f"  {label:15s}: {count}")

    # Save
    save_training_data("training/training_data.json", data)

    # Preview
    print("\n--- Sample examples ---")
    for text, ann in data[:5]:
        print(f"\nText: {text}")
        print(f"  Entities: {ann['entities']}")
