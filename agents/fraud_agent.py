def analyze_fraud(transaction, customer):
    
    fraud_score = 0
    reasons = []

    # Check device
    if transaction["device"] == "UNKNOWN":
        fraud_score += 2
        reasons.append(
            "Transaction was made from an unknown device."
        )

    # Check location
    if transaction["location"] != customer["city"]:
        fraud_score += 2
        reasons.append(
            "Transaction location does not match customer's registered city."
        )

    # Check customer risk level
    if customer["risk_level"] == "HIGH":
        fraud_score += 2
        reasons.append(
            "Customer already has a high risk profile."
        )

    elif customer["risk_level"] == "MEDIUM":
        fraud_score += 1
        reasons.append(
            "Customer has a medium risk profile."
        )

    # Final fraud decision
    if fraud_score >= 4:
        fraud_risk = "HIGH"
        suspicious = "YES"

    elif fraud_score >= 2:
        fraud_risk = "MEDIUM"
        suspicious = "YES"

    else:
        fraud_risk = "LOW"
        suspicious = "NO"

    # Normal transaction
    if not reasons:
        reasons.append(
            "Known device, normal location, and no major risk indicators."
        )

    return {
        "fraud_score": fraud_score,
        "fraud_risk": fraud_risk,
        "suspicious": suspicious,
        "reason": " ".join(reasons)
    }