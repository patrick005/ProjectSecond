// DB_manager.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>
#include <zmq.h> // ZMQ 라이브러리 추가
#include <errno.h> // For errno

#define DB_NAME "player_stats.db"
#define ZMQ_DB_PULL_PORT "6003" // main.py에서 PUSH할 포트

// DB 초기화 함수
void init_db(sqlite3 *db) {
    const char *sql = "CREATE TABLE IF NOT EXISTS stats ("
                      "client_ip TEXT PRIMARY KEY NOT NULL,"
                      "total INTEGER NOT NULL DEFAULT 0,"
                      "win INTEGER NOT NULL DEFAULT 0,"
                      "lose INTEGER NOT NULL DEFAULT 0);";
    char *errmsg = 0;
    if (sqlite3_exec(db, sql, 0, 0, &errmsg) != SQLITE_OK) {
        fprintf(stderr, "DB Init Error: %s\n", errmsg);
        sqlite3_free(errmsg);
    } else {
        printf("DB initialized successfully.\n");
    }
}

// 승패 업데이트 함수 (내부용)
void _update_stats(sqlite3 *db, const char *ip, int is_winner) {
    sqlite3_stmt *stmt;
    // 먼저 해당 IP가 존재하는지 확인하고 없으면 삽입
    const char *select_sql = "SELECT client_ip FROM stats WHERE client_ip = ?";
    sqlite3_prepare_v2(db, select_sql, -1, &stmt, 0);
    sqlite3_bind_text(stmt, 1, ip, -1, SQLITE_TRANSIENT);
    if (sqlite3_step(stmt) != SQLITE_ROW) { // IP가 존재하지 않으면 삽입
        const char *insert_sql = "INSERT INTO stats (client_ip, total, win, lose) VALUES (?, 0, 0, 0)";
        sqlite3_stmt *insert_stmt;
        sqlite3_prepare_v2(db, insert_sql, -1, &insert_stmt, 0);
        sqlite3_bind_text(insert_stmt, 1, ip, -1, SQLITE_TRANSIENT);
        if (sqlite3_step(insert_stmt) != SQLITE_DONE) {
            fprintf(stderr, "DB Insert Error: %s\n", sqlite3_errmsg(db));
        }
        sqlite3_finalize(insert_stmt);
    }
    sqlite3_finalize(stmt);

    // 승/패 업데이트
    const char *update_sql = is_winner
        ? "UPDATE stats SET win = win + 1, total = total + 1 WHERE client_ip = ?"
        : "UPDATE stats SET lose = lose + 1, total = total + 1 WHERE client_ip = ?";
    sqlite3_prepare_v2(db, update_sql, -1, &stmt, 0);
    sqlite3_bind_text(stmt, 1, ip, -1, SQLITE_TRANSIENT);
    if (sqlite3_step(stmt) != SQLITE_DONE) {
        fprintf(stderr, "DB Update Error: %s\n", sqlite3_errmsg(db));
    }
    sqlite3_finalize(stmt);
    printf("Stats updated for IP: %s (Winner: %d)\n", ip, is_winner);
}

// 무승부 처리 함수 (내부용)
void _update_draw(sqlite3 *db, const char *ip) {
    sqlite3_stmt *stmt;
    // 먼저 해당 IP가 존재하는지 확인하고 없으면 삽입
    const char *select_sql = "SELECT client_ip FROM stats WHERE client_ip = ?";
    sqlite3_prepare_v2(db, select_sql, -1, &stmt, 0);
    sqlite3_bind_text(stmt, 1, ip, -1, SQLITE_TRANSIENT);
    if (sqlite3_step(stmt) != SQLITE_ROW) { // IP가 존재하지 않으면 삽입
        const char *insert_sql = "INSERT INTO stats (client_ip, total, win, lose) VALUES (?, 0, 0, 0)";
        sqlite3_stmt *insert_stmt;
        sqlite3_prepare_v2(db, insert_sql, -1, &insert_stmt, 0);
        sqlite3_bind_text(insert_stmt, 1, ip, -1, SQLITE_TRANSIENT);
        if (sqlite3_step(insert_stmt) != SQLITE_DONE) {
            fprintf(stderr, "DB Insert Error: %s\n", sqlite3_errmsg(db));
        }
        sqlite3_finalize(insert_stmt);
    }
    sqlite3_finalize(stmt);

    // 무승부 업데이트 (total만 증가)
    const char *update_sql = "UPDATE stats SET total = total + 1 WHERE client_ip = ?";
    sqlite3_prepare_v2(db, update_sql, -1, &stmt, 0);
    sqlite3_bind_text(stmt, 1, ip, -1, SQLITE_TRANSIENT);
    if (sqlite3_step(stmt) != SQLITE_DONE) {
        fprintf(stderr, "DB Update Error: %s\n", sqlite3_errmsg(db));
    }
    sqlite3_finalize(stmt);
    printf("Draw stats updated for IP: %s\n", ip);
}

// ZMQ 메시지를 수신하고 DB 업데이트를 처리하는 메인 루프
void start_db_service(sqlite3 *db) {
    void *context = zmq_ctx_new();
    void *receiver = zmq_socket(context, ZMQ_PULL); // PULL 소켓으로 변경
    int rc = zmq_bind(receiver, "tcp://*:" ZMQ_DB_PULL_PORT); // DB_PULL_PORT에 바인딩
    if (rc != 0) {
        fprintf(stderr, "ZMQ Bind Error: %s\n", zmq_strerror(errno));
        zmq_close(receiver);
        zmq_ctx_destroy(context);
        return;
    }
    printf("C DB Service started, waiting for messages on tcp://*:%s\n", ZMQ_DB_PULL_PORT);

    while (1) {
        zmq_msg_t message;
        zmq_msg_init(&message);
        if (zmq_msg_recv(&message, receiver, 0) == -1) {
            fprintf(stderr, "ZMQ Receive Error: %s\n", zmq_strerror(errno));
            zmq_msg_close(&message);
            break;
        }

        char *buffer = (char*)zmq_msg_data(&message);
        size_t len = zmq_msg_size(&message);
        // Ensure buffer is null-terminated before sscanf.
        // It's safer to copy to a local buffer with known size.
        char local_buffer[256]; // Sufficiently large buffer
        if (len >= sizeof(local_buffer)) {
            len = sizeof(local_buffer) - 1; // Truncate if too long
        }
        memcpy(local_buffer, buffer, len);
        local_buffer[len] = '\0'; // Null-terminate

        printf("[C DB Service] Received: %s\n", local_buffer);

        char ip_str[64];
        char result_str[16];
        // 메시지 파싱: "IP,RESULT_TYPE" 형식 (예: "192.168.0.100,WIN")
        if (sscanf(local_buffer, "%63[^,],%15s", ip_str, result_str) == 2) {
            if (strcmp(result_str, "WIN") == 0) {
                _update_stats(db, ip_str, 1);
            } else if (strcmp(result_str, "LOSE") == 0) {
                _update_stats(db, ip_str, 0);
            } else if (strcmp(result_str, "DRAW") == 0) {
                _update_draw(db, ip_str);
            } else {
                fprintf(stderr, "Unknown result type: %s\n", result_str);
            }
        } else {
            fprintf(stderr, "Invalid message format: %s\n", local_buffer);
        }
        zmq_msg_close(&message);
    }

    zmq_close(receiver);
    zmq_ctx_destroy(context);
}

int main() {
    sqlite3 *db;
    // SQLite DB 파일 열기
    if (sqlite3_open(DB_NAME, &db)) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return 1;
    }

    init_db(db); // DB 스키마 초기화
    start_db_service(db); // ZMQ 메시지 수신 및 DB 업데이트 시작

    sqlite3_close(db); // DB 닫기
    return 0;
}
