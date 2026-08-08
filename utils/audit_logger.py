import csv
import os
from datetime import datetime


def log_action(
    transaction_id,
    customer_id,
    agent,
    action,
    amount,
    risk_level,
    decision,
    reason
):
    file_path = "logs/audit_log.csv"

    # Create logs folder if it does not exist
    os.makedirs("logs", exist_ok=True)

    # Check whether file already has content
    file_exists = (
        os.path.isfile(file_path)
        and os.path.getsize(file_path) > 0
    )

    with open(
        file_path,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # Add header only for new/empty file
        if not file_exists:
            writer.writerow([
                "timestamp",
                "transaction_id",
                "customer_id",
                "agent",
                "action",
                "amount",
                "risk_level",
                "decision",
                "reason"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            transaction_id,
            customer_id,
            agent,
            action,
            amount,
            risk_level,
            decision,
            reason
        ])


def get_existing_decision(transaction_id):
    file_path = "logs/audit_log.csv"

    # No audit log yet
    if not os.path.isfile(file_path):
        return None

    # Empty audit log
    if os.path.getsize(file_path) == 0:
        return None

    with open(
        file_path,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            if row["transaction_id"] == transaction_id:
                return row["decision"]

    return None