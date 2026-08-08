def analyze_payment(transaction):
    
    status = transaction["status"]
    debit_status = transaction["debit_status"]
    amount = transaction["amount"]

    # Case 1: Payment failed and money was deducted
    if status == "FAILED" and debit_status == "DEBITED":

        recommendation = "REFUND"
        reason = "Payment failed but the customer's account was debited."

    # Case 2: Payment failed but money was NOT deducted
    elif status == "FAILED" and debit_status == "NOT_DEBITED":

        recommendation = "NO REFUND REQUIRED"
        reason = "Payment failed, but no money was deducted from the customer."

    # Case 3: Payment is still pending
    elif status == "PENDING":

        recommendation = "MONITOR TRANSACTION"
        reason = "Transaction is still pending and should be monitored."

    # Case 4: Successful payment
    elif status == "SUCCESS":

        recommendation = "NO ACTION REQUIRED"
        reason = "Transaction was completed successfully."

    else:

        recommendation = "MANUAL REVIEW"
        reason = "Transaction status requires manual investigation."

    return {
        "recommendation": recommendation,
        "reason": reason,
        "amount": amount
    }