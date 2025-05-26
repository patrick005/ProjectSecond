# 데이터베이스 목록

# 데이터베이스 내 테이블 목록  
| Tables_in_SecondProject |
|-------------------------|
| stats                   |

# 테이블의 속성  
| Field     | Type     | Key & Null           | Default  | Description                     |
|--------------|----------|---------------------|---------|--------------------------|
| client_ip    | TEXT     | PRIMARY KEY, NOT NULL | 없음    | 클라이언트의 IP 주소 (식별자) |
| total        | INTEGER  | NOT NULL            | 0       | 총 게임 참여 횟수             |
| win          | INTEGER  | NOT NULL            | 0       | 승리 횟수                   |
| lose         | INTEGER  | NOT NULL            | 0       | 패배 횟수                   |
