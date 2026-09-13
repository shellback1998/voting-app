import os
import time

import psycopg
import redis


# --------------------------------------------------
# Configuration
# --------------------------------------------------
#
# Database credentials are supplied through
# environment variables rather than stored directly
# in the source code.
#

postgres_password = os.environ["POSTGRES_PASSWORD"]


# --------------------------------------------------
# Connect to Redis
# --------------------------------------------------

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)


# --------------------------------------------------
# Connect to PostgreSQL
# --------------------------------------------------
#
# PostgreSQL may take a few seconds to start.
# The worker keeps trying until the database
# becomes available.
#

while True:

    try:

        db = psycopg.connect(
            host="db",
            dbname="votes",
            user="postgres",
            password=postgres_password
        )

        cursor = db.cursor()

        # Create the votes table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id SERIAL PRIMARY KEY,
                vote VARCHAR(50) NOT NULL
            )
        """)

        db.commit()

        print("Connected to PostgreSQL.")

        break

    except psycopg.OperationalError:

        print("Waiting for PostgreSQL...")

        time.sleep(2)


print("Worker started. Waiting for votes...")


# --------------------------------------------------
# Process votes
# --------------------------------------------------
#
# BLPOP waits for an item to appear in the
# Redis list named "votes".
#
# When a vote appears, the worker removes it
# from Redis and inserts it into PostgreSQL.
#

while True:

    vote = redis_client.blpop(
        "votes",
        timeout=5
    )

    if vote:

        choice = vote[1]

        cursor.execute(
            "INSERT INTO votes (vote) VALUES (%s)",
            (choice,)
        )

        db.commit()

        print(f"Stored vote: {choice}")