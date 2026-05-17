import time
from fastapi import FastAPI
from pydantic import BaseModel

from detectors.rule_detector import detect_rule_attack
from detectors.semantic_detector import semantic_score
from utils.language import detect_language
from pii.presidio_custom import analyze_pii, anonymize_text
from policy.policy_engine import make_decision
from utils.logging_utils import write_audit_log


# -----------------------------
# App Initialization
# -----------------------------
app = FastAPI(title="LLM Security Gateway")


# -----------------------------
# Request Schema
# -----------------------------
class AnalyzeRequest(BaseModel):
    text: str


# -----------------------------
# Core API Endpoint
# -----------------------------
@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    # -----------------------------
    # Start latency timer
    # -----------------------------
    start_time = time.time()

    text = data.text

    # -----------------------------
    # PIPELINE: DETECTION LAYERS
    # -----------------------------
    lang = detect_language(text)

    rule_score = detect_rule_attack(text)

    sem_score = semantic_score(text)

    pii_results = analyze_pii(text)
    pii_found = len(pii_results) > 0

    decision = make_decision(
        rule_score,
        sem_score,
        pii_found
    )

    # -----------------------------
    # SAFE OUTPUT HANDLING
    # -----------------------------
    safe_text = text

    if decision == "MASK":
        safe_text = anonymize_text(text, pii_results)

    if decision == "BLOCK":
        safe_text = None

    # -----------------------------
    # LATENCY MEASUREMENT
    # -----------------------------
    latency_ms = round((time.time() - start_time) * 1000, 2)

    # -----------------------------
    # AUDIT LOGGING
    # -----------------------------
    log_entry = {
        "language": lang,
        "rule_score": rule_score,
        "semantic_score": sem_score,
        "decision": decision,
        "latency_ms": latency_ms
    }

    write_audit_log(log_entry)

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------
    return {
        "language": lang,
        "rule_score": rule_score,
        "semantic_score": sem_score,
        "decision": decision,
        "safe_text": safe_text,
        "latency_ms": latency_ms
    }
