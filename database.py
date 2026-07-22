import aiosqlite


class Database:
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
        self.conn = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.db_path)

        await self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS "users" (
                "id"	INTEGER NOT NULL UNIQUE,
                "username"	TEXT,
                "discord_user_id"	TEXT NOT NULL UNIQUE,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            CREATE TABLE IF NOT EXISTS "events" (
                "id"	INTEGER NOT NULL UNIQUE,
                "name"	TEXT NOT NULL,
                "roles"	TEXT NOT NULL,
                "start_date"	TEXT,
                "end_date"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            CREATE TABLE IF NOT EXISTS "user_participates_in_event" (
                "user_id"	INTEGER NOT NULL,
                "event_id"	INTEGER NOT NULL,
                FOREIGN KEY("event_id") REFERENCES "events"("id"),
                FOREIGN KEY("user_id") REFERENCES "users"("id") ON UPDATE CASCADE
            );
            CREATE TABLE IF NOT EXISTS "profile_ratings" (
                "id"	INTEGER NOT NULL UNIQUE,
                "judge_user_id"	INTEGER NOT NULL,
                "rated_user_id"	INTEGER NOT NULL,
                "cards"	REAL DEFAULT 0,
                "cr"	REAL DEFAULT 0,
                "cl"	REAL DEFAULT 0,
                "skill"	REAL DEFAULT 0,
                "tiers"	REAL DEFAULT 0,
                "best_teams"	REAL DEFAULT 0,
                "kizna"	REAL DEFAULT 0,
                "oshi"	REAL DEFAULT 0,
                "profile"	REAL DEFAULT 0,
                "avg"	REAL DEFAULT 0,
                PRIMARY KEY("id" AUTOINCREMENT),
                FOREIGN KEY("judge_user_id") REFERENCES "users"("id") ON UPDATE CASCADE,
                FOREIGN KEY("rated_user_id") REFERENCES "users"("id") ON UPDATE CASCADE
            );
        """)

        await self.conn.commit()
        print("Database connection established and any missing tables created")

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def getEventRoles(self, event):
        async with self.conn.execute(
            "SELECT roles FROM events WHERE name = ?", (event,)
        ) as cursor:
            row = await cursor.fetchone()
            if row and row[0]:
                return row[0].split()
            return []
