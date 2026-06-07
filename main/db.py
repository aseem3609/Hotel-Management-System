"""Central database helper for the Hotel Management System.

Keeps the MySQL connection details in one place so the rest of the
application does not repeat the host/user/password on every call.
"""

import os
import mysql.connector

# ---------------------------------------------------------------------------
# Connection settings
# ---------------------------------------------------------------------------
DB_CONFIG = {
    "host": os.environ.get("HMS_DB_HOST", "localhost"),
    "user": os.environ.get("HMS_DB_USER", "root"),
    "password": os.environ.get("HMS_DB_PASSWORD", "AshimtiW@07"),
    "database": os.environ.get("HMS_DB_NAME", "hotel_management_system"),
}


def get_connection():
    """Return a new MySQL connection using the shared configuration."""
    return mysql.connector.connect(**DB_CONFIG)


def ensure_schema():
    """Make sure optional columns used by newer features exist.

    Safe to call multiple times; it only adds the `Status` column to the
    `room` table when it is missing so existing databases keep working.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.columns "
            "WHERE table_schema=%s AND table_name='room' AND column_name='Status'",
            (DB_CONFIG["database"],),
        )
        exists = cursor.fetchone()[0]
        if not exists:
            cursor.execute(
                "ALTER TABLE room ADD COLUMN `Status` VARCHAR(20) "
                "NOT NULL DEFAULT 'Checked-in'"
            )
            connection.commit()
        connection.close()
    except Exception as es:  # pragma: no cover - best effort migration
        print(f"[db] ensure_schema skipped: {es}")


def ensure_reviews_table():
    """Create the `reviews` table if it does not already exist.

    Stores customer feedback together with the sentiment label and score
    produced by the sentiment-analysis model.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS reviews ("
            "  id INT AUTO_INCREMENT PRIMARY KEY,"
            "  customer_contact VARCHAR(20),"
            "  customer_name VARCHAR(100),"
            "  rating INT,"
            "  review_text TEXT,"
            "  sentiment VARCHAR(20),"
            "  sentiment_score FLOAT,"
            "  created_at DATETIME"
            ")"
        )
        connection.commit()
        connection.close()
    except Exception as es:  # pragma: no cover - best effort migration
        print(f"[db] ensure_reviews_table skipped: {es}")


# Folder where generated PDF invoices are written.
INVOICE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "invoices")
os.makedirs(INVOICE_DIR, exist_ok=True)
