import streamlit as st
import pandas as pd
import os
import csv

from agents.payment_agent import analyze_payment
from agents.fraud_agent import analyze_fraud
from agents.orchestrator import orchestrate
from agents.support_agent import analyze_support
from utils.risk_checker import check_risk
from utils.audit_logger import log_action, get_existing_decision



# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Financial Operations Assistant",
    page_icon="💳",
    layout="wide"
)

role = st.sidebar.selectbox(
    "Select Role",
    ["Analyst", "Approver", "Admin"]
)

st.title("💳 Agentic Financial Operations Assistant")
st.write("AI-powered assistant for financial operations")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

transactions = pd.read_csv("data/transactions.csv")
customers = pd.read_csv("data/customers.csv")
support_tickets = pd.read_csv("data/support_tickets.csv")


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "selected_transaction" not in st.session_state:
    st.session_state.selected_transaction = None

if "decision" not in st.session_state:
    st.session_state.decision = None


# --------------------------------------------------
# TRANSACTION CHECKER
# --------------------------------------------------

st.subheader("🔍 Transaction Checker")

transaction_id = st.text_input(
    "Enter Transaction ID",
    placeholder="Example: TXN001"
)


if st.button("Check Transaction"):

    entered_id = transaction_id.strip().upper()

    result = transactions[
        transactions["transaction_id"] == entered_id
    ]

    if not result.empty:

        st.session_state.selected_transaction = entered_id
        st.session_state.decision = None

    else:

        st.session_state.selected_transaction = None
        st.session_state.decision = None

        st.error("❌ Transaction not found")


# --------------------------------------------------
# DISPLAY SELECTED TRANSACTION
# --------------------------------------------------

if st.session_state.selected_transaction:

    result = transactions[
        transactions["transaction_id"]
        == st.session_state.selected_transaction
    ]

    transaction = result.iloc[0]

    st.success("✅ Transaction Found")


    # --------------------------------------------------
    # TRANSACTION SUMMARY
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Amount",
            f"₹{transaction['amount']}"
        )

    with col2:
        st.metric(
            "Status",
            transaction["status"]
        )

    with col3:
        st.metric(
            "Customer ID",
            transaction["customer_id"]
        )


    # --------------------------------------------------
    # TRANSACTION DETAILS
    # --------------------------------------------------

    st.subheader("💳 Transaction Details")

    st.write(
        "**Transaction ID:**",
        transaction["transaction_id"]
    )

    st.write(
        "**Payment Type:**",
        transaction["type"]
    )

    st.write(
        "**Debit Status:**",
        transaction["debit_status"]
    )

    st.write(
        "**Location:**",
        transaction["location"]
    )

    st.write(
        "**Device:**",
        transaction["device"]
    )


    # --------------------------------------------------
    # CUSTOMER DETAILS
    # --------------------------------------------------

    customer_result = customers[
        customers["customer_id"]
        == transaction["customer_id"]
    ]

    if not customer_result.empty:

        customer = customer_result.iloc[0]

        st.subheader("👤 Customer Details")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(
                "**Name:**",
                customer["name"]
            )

        with col2:
            st.write(
                "**Account Type:**",
                customer["account_type"]
            )

        with col3:
            st.write(
                "**Risk Level:**",
                customer["risk_level"]
            )

        st.write(
            "**City:**",
            customer["city"]
        )

    else:

        st.warning("Customer details not found")


    # --------------------------------------------------
    # SUPPORT TICKET
    # --------------------------------------------------

    ticket_result = support_tickets[
        support_tickets["transaction_id"]
        == transaction["transaction_id"]
    ]

    if not ticket_result.empty:

        ticket = ticket_result.iloc[0]

        st.subheader("🎫 Support Ticket")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(
                "**Ticket ID:**",
                ticket["ticket_id"]
            )

        with col2:
            st.write(
                "**Status:**",
                ticket["status"]
            )

        with col3:
            st.write(
                "**Priority:**",
                ticket["priority"]
            )

        st.write(
            "**Issue:**",
            ticket["issue"]
        )

    else:

        st.info(
            "No support ticket found for this transaction"
        )


    # --------------------------------------------------
    # PAYMENT AGENT
    # --------------------------------------------------

    payment_analysis = analyze_payment(transaction)

    st.subheader("🤖 Payment Agent Analysis")

    st.write(
        "**Recommendation:**",
        payment_analysis["recommendation"]
    )

    st.write(
        "**Reason:**",
        payment_analysis["reason"]
    )

    # --------------------------------------------------
    # FRAUD AGENT
    # --------------------------------------------------

    if not customer_result.empty:

        fraud_analysis = analyze_fraud(
            transaction,
            customer
        )

        st.subheader("🕵️ Fraud Agent Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Fraud Risk",
                fraud_analysis["fraud_risk"]
            )

        with col2:
            st.metric(
                "Suspicious",
                fraud_analysis["suspicious"]
            )

        with col3:
            st.metric(
                "Fraud Score",
                fraud_analysis["fraud_score"]
            )

        st.write(
            "**Reason:**",
            fraud_analysis["reason"]
        )

        # --------------------------------------------------
        # ORCHESTRATOR AGENT
        # --------------------------------------------------

        orchestration = orchestrate(
            payment_analysis,
            fraud_analysis
        )

        st.subheader("🧠 Orchestrator Agent")

        st.write(
            "**Final Action:**",
            orchestration["final_action"]
        )

        st.write(
            "**Reason:**",
            orchestration["reason"]
        )

        # --------------------------------------------------
        # SUPPORT AGENT
        # --------------------------------------------------

        if not ticket_result.empty:

            support_analysis = analyze_support(
                ticket,
                payment_analysis,
                fraud_analysis,
                orchestration
            )

            st.subheader("🎧 Support Agent")

            with st.expander("View complete AI decision process"):

                st.write("### 💳 Payment Agent")
                st.write("**Decision:**", payment_analysis["recommendation"])
                st.write("**Reason:**", payment_analysis["reason"])

                st.divider()

                st.write("### 🕵️ Fraud Agent")
                st.write("**Fraud Risk:**", fraud_analysis["fraud_risk"])
                st.write("**Fraud Score:**", fraud_analysis["fraud_score"])
                st.write("**Reason:**", fraud_analysis["reason"])

                st.divider()

                st.write("### 🎯 Orchestrator")
                st.write("**Final Action:**", orchestration["final_action"])
                st.write("**Reason:**", orchestration["reason"])

            st.write(
                "**Customer Issue:**",
                support_analysis["issue"]
            )

            st.write(
                "**Recommended Resolution:**",
                support_analysis["resolution"]
            )

            st.write(
                "**✨ AI Generated Response:**",
                support_analysis["ai_resolution"]
            )
            if support_analysis["ai_response_safe"]:
                    st.success("🛡️ AI Guardrail: Response validated as safe.")

            else:
                st.warning(
                    "🛡️ AI Guardrail activated: "
                    "An unverified financial claim was blocked."
          )

# --------------------------------------------------
# AGENT DECISION TRACE
# --------------------------------------------------
if 'payment_analysis' in locals():
    st.subheader("🧠 Agent Decision Trace")

    with st.expander("View complete AI decision process"):

        st.write("### 💳 Payment Agent")
        st.write(
            "**Decision:**",
            payment_analysis["recommendation"]
        )
        st.write(
            "**Reason:**",
            payment_analysis["reason"]
        )

        st.divider()

        st.write("### 🕵️ Fraud Agent")
        st.write(
            "**Fraud Risk:**",
            fraud_analysis["fraud_risk"]
        )
        st.write(
            "**Fraud Score:**",
            fraud_analysis["fraud_score"]
        )
        st.write(
            "**Reason:**",
            fraud_analysis["reason"]
        )

        st.divider()

        st.write("### 🧠 Orchestrator Agent")
        st.write(
            "**Final Action:**",
            orchestration["final_action"]
        )
        st.write(
            "**Reason:**",
            orchestration["reason"]
        )

        st.divider()

        st.write("### 🎧 Support Agent")
        st.write(
            "**Resolution:**",
            support_analysis["resolution"]
        )

        st.divider()

        st.write("### 🛡️ AI Guardrail")

        if support_analysis["ai_response_safe"]:
            st.success("AI response passed safety validation.")
        else:
            st.warning("Unsafe financial claim detected and blocked.")
            st.write(
                "**Blocked Reason:**",
                support_analysis["blocked_reason"]
            )

# --------------------------------------------------
# FINAL DECISION SUMMARY
# --------------------------------------------------

#st.subheader("🎯 Final Decision Summary")

#col1, col2, col3 = st.columns(3)

#with col1:
 #   st.metric(
  #      "Final Action",
   #     orchestration["final_action"]
    #)

#with col2:
 #   st.metric(
  #      "Fraud Risk",
    #    fraud_analysis["fraud_risk"]
    #)

#with col3:
 #   guardrail_status = (
  #      "PASSED"
   #     if support_analysis["ai_response_safe"]
    #    else "BLOCKED"
    #)

    #st.metric(
     #   "AI Guardrail",
      #  guardrail_status
    #)

#if orchestration["final_action"] == "PROCEED WITH REFUND":
    #st.success(
     #   "✅ System Recommendation: Transaction is eligible for refund."
    #)

#elif orchestration["final_action"] == "REFUND REQUIRES REVIEW":
 #   st.warning(
  #      "⚠️ System Recommendation: Human review required before refund."
   # )

#else:
 #   st.info(
  #      f"ℹ️ System Recommendation: {orchestration['final_action']}"
   # )


    # --------------------------------------------------
    # RISK CHECKER
    # --------------------------------------------------
    payment_analysis = analyze_payment(transaction)
    
    risk_analysis = check_risk(
        transaction["amount"],
        payment_analysis["recommendation"]
    )

    st.subheader("🛡️ Risk & Approval")

    st.write(
        "**Risk Level:**",
        risk_analysis["risk_level"]
    )


    # --------------------------------------------------
    # HUMAN APPROVAL
    # --------------------------------------------------

    if risk_analysis["approval_required"]:

        st.warning("⚠️ Human Approval Required")
        existing_decision = get_existing_decision(
            transaction["transaction_id"]
        )

        if role == "Analyst":
    
            st.warning(
                "🔒 Analyst role has read-only access. Approval actions are disabled."
            )

        else:

            col1, col2 = st.columns(2)


            # APPROVE BUTTON
            with col1:
                if st.button("✅ Approve"):

                    if existing_decision:

                        st.warning(
                            f"⚠️ Decision already recorded as "
                            f"{existing_decision} for "
                            f"{transaction['transaction_id']}. "
                            "Duplicate financial action prevented."
                        )

                    else:

                        log_action(
                            transaction["transaction_id"],
                            transaction["customer_id"],
                            "Payment Agent",
                            payment_analysis["recommendation"],
                            transaction["amount"],
                            risk_analysis["risk_level"],
                            "APPROVED",
                            payment_analysis["reason"]
                        )

                    st.success(
                        "✅ Refund approved by human reviewer "
                        "and saved to audit log."
                 )


            # REJECT BUTTON
            with col2:
                if st.button("❌ Reject"):

                    if existing_decision:

                        st.warning(
                            f"⚠️ Decision already recorded as "
                            f"{existing_decision} for "
                            f"{transaction['transaction_id']}. "
                            "Duplicate financial action prevented."
                       )

                    else:

                        log_action(
                            transaction["transaction_id"],
                            transaction["customer_id"],
                            "Payment Agent",
                            payment_analysis["recommendation"],
                            transaction["amount"],
                            risk_analysis["risk_level"],
                            "REJECTED",
                            payment_analysis["reason"]
                        )

                        st.error(
                            "❌ Action rejected by human reviewer "
                            "and saved to audit log."
                        )


        # --------------------------------------------------
        # SHOW HUMAN DECISION
        # --------------------------------------------------

        if st.session_state.decision == "APPROVED":

            st.success(
                "✅ Refund approved by human reviewer "
                "and saved to audit log."
            )

        elif st.session_state.decision == "REJECTED":

            st.error(
                "❌ Refund rejected by human reviewer "
                "and saved to audit log."
            )

    else:

        st.success(
            "✅ No human approval required."
        )


# --------------------------------------------------
# AUDIT & COMPLIANCE DASHBOARD
# --------------------------------------------------

st.divider()
st.subheader("📊 Audit & Compliance Dashboard")

audit_file = "logs/audit_log.csv"

try:
    audit_data = pd.read_csv(audit_file)

    if not audit_data.empty:

        # ------------------------------------------
        # AUDIT METRICS
        # ------------------------------------------

        total_decisions = len(audit_data)

        approved_count = (
            audit_data["decision"]
            .astype(str)
            .str.upper()
            .eq("APPROVED")
            .sum()
        )

        rejected_count = (
            audit_data["decision"]
            .astype(str)
            .str.upper()
            .eq("REJECTED")
            .sum()
        )

        high_risk_count = (
            audit_data["risk_level"]
            .astype(str)
            .str.upper()
            .eq("HIGH")
            .sum()
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Decisions", total_decisions)

        with col2:
            st.metric("Approved", approved_count)

        with col3:
            st.metric("Rejected", rejected_count)

        with col4:
            st.metric("High Risk", high_risk_count)

        st.divider()

        # ------------------------------------------
        # FILTERS
        # ------------------------------------------

        st.write("### 🔎 Audit Filters")

        filter_col1, filter_col2 = st.columns(2)

        transaction_options = (
            ["All"] +
            sorted(
                audit_data["transaction_id"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        decision_options = (
            ["All"] +
            sorted(
                audit_data["decision"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        with filter_col1:
            selected_transaction = st.selectbox(
                "Transaction",
                transaction_options
            )

        with filter_col2:
            selected_decision = st.selectbox(
                "Decision",
                decision_options
            )

        # ------------------------------------------
        # APPLY FILTERS
        # ------------------------------------------

        filtered_audit = audit_data.copy()

        if selected_transaction != "All":
            filtered_audit = filtered_audit[
                filtered_audit["transaction_id"].astype(str)
                == selected_transaction
            ]

        if selected_decision != "All":
            filtered_audit = filtered_audit[
                filtered_audit["decision"].astype(str)
                == selected_decision
            ]

        # ------------------------------------------
        # DECISION HISTORY
        # ------------------------------------------

        st.write("### 📋 Human Decision History")

        if not filtered_audit.empty:

            st.dataframe(
                filtered_audit[
                    [
                        "timestamp",
                        "transaction_id",
                        "agent",
                        "action",
                        "amount",
                        "risk_level",
                        "decision"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No audit records match the selected filters.")

    else:
        st.info("No audit records available yet.")

except FileNotFoundError:
    st.info("No audit log has been created yet.")

def get_existing_decision(transaction_id):
    
    file_path = "logs/audit_log.csv"

    # Audit file does not exist yet
    if not os.path.isfile(file_path):
        return None

    # Empty audit file
    if os.path.getsize(file_path) == 0:
        return None

    with open(file_path, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            if row["transaction_id"] == transaction_id:
                return row["decision"]

    return None