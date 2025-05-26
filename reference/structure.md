

```
graph TD
    subgraph Client [ESP8266 Device]
        C1(MPU6050 Sensor) --> C2(Client.cpp)
        C2 -- WiFi / TCP Socket --> R1[Relay Server]
        R1 -- TCP Socket --> C2
        C2 -- LED Control --> C3(RGB LEDs)
    end

    subgraph Server [Raspberry Pi]
        R1(Relay Server - relay_server.py)
        M1(Main Game Logic - main.py)
        G1(Game Logic - game_logic.py)
        Z1(ZMQ Handler - zmq_handler.py)
        D1(DB Manager - db_manager.py)
    end

    subgraph ZMQ Communication
        ZMQ_P1(ZMQ PUB Socket - Actions: 6000)
        ZMQ_S1(ZMQ SUB Socket - Actions)
        ZMQ_P2(ZMQ PUB Socket - Game Flags: 6001)
        ZMQ_S2(ZMQ SUB Socket - Game Flags)
    end

    C2 -- "1. TCP: ATTACK/MOVEMENT/ACCEPT" --> R1
    R1 -- "2. ZMQ PUB: Client IP, Action" --> ZMQ_P1
    ZMQ_P1 -- "3. ZMQ Network" --> ZMQ_S1
    ZMQ_S1 --> M1

    M1 -- "4. Game State Decision (Start/End)" --> ZMQ_P2
    ZMQ_P2 -- "5. ZMQ Network" --> ZMQ_S2
    ZMQ_S2 --> R1

    R1 -- "6. TCP: Game Flag (0/1)" --> C2

    M1 -- "7. Call Game Logic (process_round, reset_game)" --> G1
    G1 -- "8. Update Player Stats" --> D1
    D1 -- "9. SQLite DB" --> D1

    subgraph Client Startup Process
        C_Start(Client Startup) --> C_WiFi(Connect WiFi)
        C_WiFi --> C_MPU(Init MPU6050)
        C_MPU --> C_TCP(Connect TCP to Relay Server)
        C_TCP -- Initial Game Flag (0/1) --> C_Loop(Loop - Monitor MPU & TCP)
        C_Loop --> C_LED(Update LEDs)
    end

    subgraph Relay Server Startup Process
        R_Start(Relay Server Startup) --> R_TCP_Listen(Start TCP Listener 7755)
        R_TCP_Listen --> R_ZMQ_PUB_Bind(Bind ZMQ PUB 6000)
        R_ZMQ_PUB_Bind --> R_ZMQ_SUB_Connect(Connect ZMQ SUB 6001)
        R_ZMQ_SUB_Connect --> R_Thread(Start ZMQ Flag Monitor Thread)
        R_Thread --> R_Handle_Client_Thread(Handle new TCP client in thread)
    end

    subgraph Main Server Startup Process
        M_Start(Main Server Startup) --> M_ZMQ_SUB_Setup(Setup ZMQ SUB 6000 via zmq_handler)
        M_ZMQ_SUB_Setup --> M_ZMQ_PUB_Bind(Bind ZMQ PUB 6001)
        M_ZMQ_PUB_Bind --> M_DB_Init(Init DB)
        M_DB_Init --> M_Send_Init_Flag(Send initial Game Flag 0 via ZMQ PUB)
        M_Send_Init_Flag --> M_Loop(Main Loop - Listen ZMQ Actions)
    end

    style C2 fill:#ADD8E6,stroke:#333,stroke-width:2px
    style R1 fill:#ADD8E6,stroke:#333,stroke-width:2px
    style M1 fill:#90EE90,stroke:#333,stroke-width:2px
    style G1 fill:#90EE90,stroke:#333,stroke-width:2px
    style Z1 fill:#FFD700,stroke:#333,stroke-width:2px
    style D1 fill:#FFD700,stroke:#333,stroke-width:2px
    style C_LED fill:#D3D3D3,stroke:#333,stroke-width:1px
    style C_MPU fill:#D3D3D3,stroke:#333,stroke-width:1px
    style ZMQ_P1 fill:#FFD700,stroke:#333,stroke-width:2px
    style ZMQ_S1 fill:#FFD700,stroke:#333,stroke-width:2px
    style ZMQ_P2 fill:#FFD700,stroke:#333,stroke-width:2px
    style ZMQ_S2 fill:#FFD700,stroke:#333,stroke-width:2px
    ```
    [online flowchart maker](https://www.mermaidchart.com/)
    
  <!-- 최종때 한번 더 확인 -->