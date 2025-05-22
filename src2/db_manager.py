# db_manager.py
# DB 관련 함수
import sqlite3

#데이터베이스 연결 및 커서 생성
conn = sqlite3.connect("player_stats.db", check_same_thread=False)  #"player_stats.db"라는 로컬 파일형 SQLite 데이터베이스에 연결
cursor = conn.cursor()

#테이블 초기화 함수
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

#승패 결과 반영 함수
def update_stats(players, winner_ip):
    for ip in players:
        cursor.execute("SELECT * FROM stats WHERE client_ip = ?", (ip,))
        #해당 IP의 통계가 없을 경우 새 항목을 추가 (0으로 초기화)
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO stats (client_ip, total, win, lose) VALUES (?, 0, 0, 0)", (ip,))
        
        #승자는 win +1, 패자는 lose +1 총 경기 수(total)는 모두 +1
        if ip == winner_ip:
            cursor.execute("UPDATE stats SET win = win + 1, total = total + 1 WHERE client_ip = ?", (ip,))
        else:
            cursor.execute("UPDATE stats SET lose = lose + 1, total = total + 1 WHERE client_ip = ?", (ip,))
    conn.commit()

#무승부 반영 함수
def update_draw(players):
    for ip in players:
        cursor.execute("SELECT * FROM stats WHERE client_ip = ?", (ip,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO stats (client_ip, total, win, lose) VALUES (?, 0, 0, 0)", (ip,))
        cursor.execute("UPDATE stats SET total = total + 1 WHERE client_ip = ?", (ip,)) #무승부 발생 시 두 플레이어의 total만 +1
    conn.commit()   #DB에 반영