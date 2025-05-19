import sqlite3

conn = sqlite3.connect("player_stats.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            client_ip TEXT PRIMARY KEY NOT NULL,
            total INTEGER NOT NULL DEFAULT 0,
            win INTEGER NOT NULL DEFAULT 0,
            lose INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()

def update_stats(players, winner_ip):
    for ip in players:
        cursor.execute("SELECT * FROM stats WHERE client_ip = ?", (ip,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO stats (client_ip, total, win, lose) VALUES (?, 0, 0, 0)", (ip,))

        if ip == winner_ip:
            cursor.execute("UPDATE stats SET win = win + 1, total = total + 1 WHERE client_ip = ?", (ip,))
        else:
            cursor.execute("UPDATE stats SET lose = lose + 1, total = total + 1 WHERE client_ip = ?", (ip,))
    conn.commit()

def update_draw(players):
    for ip in players:
        cursor.execute("SELECT * FROM stats WHERE client_ip = ?", (ip,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO stats (client_ip, total, win, lose) VALUES (?, 0, 0, 0)", (ip,))
        cursor.execute("UPDATE stats SET total = total + 1 WHERE client_ip = ?", (ip,))
    conn.commit()
