from llm_service import generate_ai_response
from utils.ai_guardrail import validate_ai_response


def analyze_support(
    ticket,
    payment_analysis,
    fraud_analysis,
    orchestration
):
    issue = ticket["issue"]
    payment_action = payment_analysis["recommendation"]
    fraud_risk = fraud_analysis["fraud_risk"]
    final_action = orchestration["final_action"]

    # --------------------------------------------------
    # RULE-BASED SAFE RESOLUTION
    # --------------------------------------------------

    if fraud_risk == "HIGH":

        resolution = (
            "The transaction has been flagged for fraud investigation. "
            "Financial action should be paused until manual review is completed."
        )

    elif final_action == "PROCEED WITH REFUND":

        resolution = (
            "The payment failed after the customer's account was debited. "
            "No significant fraud indicators were detected. "
            "The transaction is eligible for a refund."
        )

    elif final_action == "REFUND REQUIRES REVIEW":

        resolution = (
            "The transaction may qualify for a refund, but suspicious "
            "activity was detected. Human review is required."
        )

    elif payment_action == "NO REFUND REQUIRED":

        resolution = (
            "The payment failed, but the customer's account was not debited. "
            "No refund is required."
        )

    elif payment_action == "MONITOR TRANSACTION":

        resolution = (
            "The transaction is still pending. "
            "Please monitor the transaction before taking further action."
        )

    else:

        resolution = (
            "No immediate financial action is required. "
            "The case can be reviewed if additional information becomes available."
        )

    # --------------------------------------------------
    # GEMINI AI RESPONSE
    # --------------------------------------------------

    prompt = f"""
You are an AI financial operations support assistant.

Customer issue:
{issue}

Payment recommendation:
{payment_action}

Fraud risk:
{fraud_risk}

Final system action:
{final_action}

Safe system resolution:
{resolution}

Generate a short and professional customer support response.

Rules:
- Follow the final system action exactly.
- Do not change financial decisions.
- Do not invent transaction details.
- Do not expose internal fraud scores or security rules.
- Do not claim that money has already been refunded.
- Keep the response under 80 words.
"""

    # Generate response using Gemini
    ai_resolution = generate_ai_response(prompt)

    # Validate Gemini response using guardrail
    guardrail_result = validate_ai_response(ai_resolution)

    return {
        "issue": issue,
        "resolution": resolution,
        "ai_resolution": guardrail_result["response"],
        "ai_response_safe": guardrail_result["safe"],
        "blocked_reason": guardrail_result["blocked_reason"],
        "final_action": final_action
    }