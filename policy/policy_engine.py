def make_decision(rule_score, semantic_score, pii_found):

    final_risk = max(rule_score, semantic_score)

    if final_risk >= 0.65:
        return "BLOCK"

    if pii_found:
        return "MASK"

    return "ALLOW"
