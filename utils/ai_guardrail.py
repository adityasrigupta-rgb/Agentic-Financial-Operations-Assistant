def validate_ai_response(ai_response):
    
    unsafe_phrases = [
        "initiated a refund",
        "refund has been initiated",
        "refund has been processed",
        "refund was processed",
        "refund completed",
        "money has been refunded",
        "funds have been refunded",
        "refund successful",
        "refund is complete",
        "funds should reflect",
        "within a few business days"
    ]

    response_lower = ai_response.lower()

    for phrase in unsafe_phrases:
        if phrase in response_lower:

            safe_response = (
                "The transaction has been reviewed and is eligible "
                "for a refund based on the current analysis. "
                "The recommended action is to proceed with the refund "
                "according to the required approval process."
            )

            return {
                "safe": False,
                "response": safe_response,
                "blocked_reason": (
                    "AI response contained an unverified financial action claim."
                )
            }

    return {
        "safe": True,
        "response": ai_response,
        "blocked_reason": None
    }