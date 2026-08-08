import redis
import psycopg2
import json
import time
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
            conn.close()
            print("✅ Database is ready!")
            break
        except Exception as e:
            print(f"⏳ Waiting for database... ({e})")
            time.sleep(1)

def init_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id VARCHAR(255) PRIMARY KEY,
                vote VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        print("✅ Table 'votes' initialized.")

def process_votes():
    redis_conn = redis.Redis(host=REDIS_HOST, db=0, socket_timeout=5)
    db_conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

    init_db(db_conn)

    print("👀 Watching vote queue...")

    while True:
        try:
            item = redis_conn.blpop("votes", timeout=0)
            if item:
                vote_json = item[1].decode("utf-8")
                vote_data = json.loads(vote_json)
                voter_id = vote_data["voter_id"]
                vote = vote_data["vote"]

                print(f"📝 Processing vote '{vote}' by '{voter_id}'")

                with db_conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO votes (id, vote) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET vote = EXCLUDED.vote",
                        (voter_id, vote)
                    )
                    db_conn.commit()
        except Exception as e:
            print(f"❌ Error processing vote: {e}")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db()
    process_votes()
