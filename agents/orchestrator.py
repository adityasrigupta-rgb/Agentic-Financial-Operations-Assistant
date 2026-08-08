def orchestrate(payment_analysis, fraud_analysis):
    
    payment_action = payment_analysis["recommendation"]
    fraud_risk = fraud_analysis["fraud_risk"]

    # High fraud risk always requires investigation
    if fraud_risk == "HIGH":
        final_action = "HOLD AND INVESTIGATE"
        reason = (
            "High fraud risk detected. Financial action should be "
            "paused until manual investigation is completed."
        )

    # Refund + suspicious transaction
    elif payment_action == "REFUND" and fraud_risk == "MEDIUM":
        final_action = "REFUND REQUIRES REVIEW"
        reason = (
            "Payment qualifies for a refund, but suspicious "
            "activity was detected."
        )

    # Normal refund
    elif payment_action == "REFUND" and fraud_risk == "LOW":
        final_action = "PROCEED WITH REFUND"
        reason = (
            "Payment qualifies for a refund and no significant "
            "fraud indicators were detected."
        )

    # No refund needed
    elif payment_action == "NO REFUND REQUIRED":
        final_action = "NO FINANCIAL ACTION"
        reason = (
            "No refund is required based on the payment analysis."
        )

    # Pending transaction
    elif payment_action == "MONITOR TRANSACTION":
        final_action = "MONITOR"
        reason = (
            "Transaction is pending and should be monitored "
            "before taking further action."
        )

    else:
        final_action = "NO ACTION REQUIRED"
        reason = (
            "No immediate financial action is required."
        )

    return {
        "final_action": final_action,
        "reason": reason
    }