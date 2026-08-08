def check_risk(amount, recommendation):
    
    # No financial action is being taken
    if recommendation != "REFUND":
        return {
            "risk_level": "LOW",
            "approval_required": False
        }

    # Refund risk based on amount
    if amount <= 5000:
        risk_level = "LOW"
        approval_required = False

    elif amount <= 10000:
        risk_level = "MEDIUM"
        approval_required = True

    else:
        risk_level = "HIGH"
        approval_required = True

    return {
        "risk_level": risk_level,
        "approval_required": approval_required
    }