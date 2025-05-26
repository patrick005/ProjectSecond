# # start_game.sh
# #!/bin/bash

# echo "Starting C DB Service (db_manager)..."

# # db_manager.c 컴파일
# echo "Compiling DB_manager.c..."
# gcc DB_manager.c -o db_manager -lsqlite3 -lzmq
# if [ $? -ne 0 ]; then
#     echo "Error: DB_manager.c compilation failed. Exiting."
#     exit 1
# fi
# echo "DB_manager.c compiled successfully."

# # db_manager 실행 파일이 현재 디렉토리에 있다고 가정
# ./db_manager &
# PIDS=($!)
# sleep 1 # C DB 서비스가 완전히 시작될 시간을 줍니다.

# echo "Starting Relay Server (relay_server.py)..."
# python3 relay_server.py &
# PIDS+=($!)
# sleep 1 # Relay Server가 포트를 바인딩할 시간을 줍니다.

# echo "Starting Main Game Logic (main.py)..."
# python3 main.py &
# PIDS+=($!)
# sleep 1 # Main Game Logic이 ZMQ 소켓을 바인딩하고 연결할 시간을 줍니다.

# # echo "Starting GUI (gui.py)..."
# python3 gui.py &
# PIDS+=($!)

# echo "All components started. Press [Enter] to stop them."
# read -r # 사용자가 Enter를 누를 때까지 대기

# echo "Stopping components..."
# # kill $DB_PID
# # kill $RELAY_PID
# # kill $MAIN_PID
# # kill $GUI_PID
# # 모든 백그라운드 프로세스 강제 종료
# for pid in "${PIDS[@]}"; do
#     if kill -0 "$pid" 2>/dev/null; then # 프로세스가 아직 실행 중인지 확인
#         echo "Killing process $pid..."
#         kill -9 "$pid" # 강제 종료 시도
#     else
#         echo "Process $pid already stopped or not found."
#     fi
# done

# echo "All components stopped."


#######################################################################1~52
#!/bin/bash

echo "Starting C DB Service (db_manager)..."

# db_manager.c 컴파일
echo "Compiling DB_manager.c..."
gcc DB_manager.c -o db_manager -lsqlite3 -lzmq
if [ $? -ne 0 ]; then
    echo "Error: DB_manager.c compilation failed. Exiting."
    exit 1
fi
echo "DB_manager.c compiled successfully."

# db_manager 실행 파일이 현재 디렉토리에 있다고 가정
./db_manager &
PIDS=($!)
sleep 1 # C DB 서비스가 완전히 시작될 시간을 줍니다.

echo "Starting Relay Server (relay_server.py)..."
python3 relay_server.py &
PIDS+=($!)
sleep 1 # Relay Server가 포트를 바인딩할 시간을 줍니다.

echo "Starting Main Game Logic (main.py)..."
python3 main.py &
PIDS+=($!)
sleep 1 # Main Game Logic이 ZMQ 소켓을 바인딩하고 연결할 시간을 줍니다.

# echo "Starting GUI (gui.py)..." # gui.py는 이제 main.py에 의해 직접 실행되므로 이 라인을 주석 처리하거나 제거
# python3 gui.py &
# PIDS+=($!) # PIDS에서도 제거

echo "All components started. Press [Enter] to stop them."
read -r # 사용자가 Enter를 누를 때까지 대기

echo "Stopping components..."
for pid in "${PIDS[@]}"; do
    if kill -0 "$pid" 2>/dev/null; then # 프로세스가 아직 실행 중인지 확인
        echo "Killing process $pid..."
        kill -9 "$pid" # 강제 종료 시도
    else
        echo "Process $pid already stopped or not found."
    fi
done

echo "All components stopped."
