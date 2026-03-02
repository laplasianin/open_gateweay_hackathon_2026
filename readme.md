## Architecture Flow Step 1

1. ** If the user is eligible and inside a designated zone, the Quality on Demand (QoD) API applies a priority policy on the Operator Network, impacting the network interaction for both staff and general users.

```mermaid
flowchart LR

    %% ===== External Platform =====
    subgraph EA["Event Platform (StageFlow)"]
        Admin["Admin UI"]
        DB[(Database)]
        StaffApp["Staff Mobile App"]
    end

    %% ===== Nokia Network as Code =====
    subgraph Nokia["Nokia Network as Code"]
        Loc["Location Verification API"]
        Geo["Geofencing API (optional)"]
        QoD["Quality on Demand API"]
    end

    %% ===== Admin setup =====
    Admin -->|Create events, zones, roles| DB
    Admin -->|Assign users to roles| DB

    %% ===== Staff login =====
    StaffApp -->|Login / get profile| DB
    StaffApp -->|Trigger location check| Admin

    %% ===== Location verification =====
    Admin -->|Verify location| Loc
    Admin -->|Check zone membership| Geo

    %% ===== QoD activation =====
    Admin -->|If eligible & inside zone| QoD
    QoD -->|Apply priority policy| Telco["Operator Network"]

    %% ===== Network impact =====
    Telco --> Crowd["General users"]
    Telco --> Staff["Staff with Priority QoD"]

    %% ===== Monitoring =====
    Admin -->|Audit logs| DB
    StaffApp <-->|QoD status ON/OFF| Admin
```


## Architecture Flow Step 2
### Staff control

<img width="1536" height="1024" alt="ChatGPT Image 2 мар  2026 г , 14_00_32" src="https://github.com/user-attachments/assets/fef64484-b23e-430d-bc17-6cd3e42d0d98" />


```mermaid
sequenceDiagram
    participant StaffApp
    participant Network
    participant Backend
    participant RulesEngine
    participant NotificationService
    participant Supervisor

    StaffApp->>Network: Location update
    Network->>Backend: Location event
    Backend->>RulesEngine: Validate zone assignment
    RulesEngine-->>Backend: Zone violation detected

    Backend->>NotificationService: Send warning to staff
    NotificationService->>StaffApp: Out of zone alert

    alt Staff returns to zone
        StaffApp->>Network: Updated location
        Network->>Backend: Location event
        Backend->>RulesEngine: Revalidate
        RulesEngine-->>Backend: Back in assigned zone
        Backend->>NotificationService: Close incident
    else Staff does not return
        Backend->>NotificationService: Escalate incident
        NotificationService->>Supervisor: Escalation alert
    end
```

#### Scenario 1

```mermaid
flowchart LR

A[Event is running normally] --> B[Police officer assigned to Sector 1]

B --> C[Officer leaves assigned zone]

C --> D[System detects out of zone movement]

D --> E[Notification sent to officer]

E --> F{Does the officer return}

F -->|Yes| G[System confirms return and closes case]

F -->|No| H[Escalation triggered]

H --> I[Supervisor receives alert and takes action]
```

#### Scenario 2

```mermaid
sequenceDiagram
    participant CrowdMonitoring
    participant Backend
    participant AI
    participant NotificationService
    participant Officer
    participant Supervisor

    CrowdMonitoring->>Backend: Increased density signal
    Backend->>AI: Analyze crowd condition
    AI-->>Backend: Recommend 2 additional officers

    Backend->>NotificationService: Assign task to nearest officers
    NotificationService->>Officer: Move to Sector 1

    alt Officers confirm and move
        Officer->>NotificationService: Task acknowledged
        Officer->>Backend: Arrival confirmed
        Backend->>AI: Update status
        AI-->>Backend: Situation stabilizing
    else No confirmation
        Backend->>NotificationService: Escalate task
        NotificationService->>Supervisor: Escalation alert
    end
```
   
```mermaid
flowchart LR

A[Event begins] --> B[People density increases in Sector 1]

B --> C[System detects abnormal crowd growth]

C --> D[AI analyzes situation]

D --> E[Decision to send 2 police officers]

E --> F[Nearest available officers receive task]

F --> G{Do officers confirm}

G -->|Yes| H[Officers move to Sector 1]

H --> I[System verifies presence and stabilizes situation]

G -->|No| J[Escalation to shift supervisor]
```

```mermaid
flowchart TB

%% =========================
%% Admin Configuration
%% =========================
subgraph Admin["Admin & Configuration"]
    AP["Admin Panel<br/>- Zones editor<br/>- Roles & Groups<br/>- Rules: where/when/what<br/>- Manual override tasks"]
    RDB[("Rules DB<br/>zones, roles, schedules,<br/>actions, escalation")]
    AP -->|CRUD rules| RDB
end

%% =========================
%% Nokia Network APIs
%% =========================
subgraph Nokia["Nokia Network APIs"]
    LOC["Location / Geofencing"]
    PRES["Device online/offline (presence)"]
    LVER["Location verification"]
    QOD["QoD Priority (optional)"]
    QOE["Throughput / QoE signals (optional)"]
end

%% =========================
%% Backend Real-time Layer
%% =========================
subgraph Backend["Real-time Processing (Python Backend)"]
    SUB["Location Stream Subscriber<br/>(webhook / poll)<br/>normalize events"]
    RULES["Rules Engine<br/>(role + time + zone)<br/>-> expected state<br/>-> violations"]
    AI["AI Decision Agent<br/>crowd / risk analysis<br/>recommendations<br/>escalation"]
    NOTIF["Notification Service<br/>push / SMS / voice<br/>ack / retry<br/>escalation chain"]
    AUD[("Audit Log / Analytics<br/>incidents<br/>KPIs<br/>heatmaps")]
end

%% =========================
%% Staff Side
%% =========================
subgraph Field["Field Execution"]
    APP["Staff Mobile App<br/>login / role<br/>receive tasks<br/>ack / complete"]
    SUP["Shift Supervisor<br/>(escalation target)"]
end

%% =========================
%% Data Flow
%% =========================

%% Nokia -> Backend
LOC -->|location events| SUB
PRES -->|presence events| SUB
LVER -->|verify in-zone| RULES
QOE -->|network signals| AI

%% Rules loading
RDB -->|load active rules| RULES

%% Processing pipeline
SUB -->|normalized events| RULES
RULES -->|violations / tasks| AI
RULES -->|simple violations| NOTIF
AI -->|decisions: move staff / open gates| NOTIF

%% Notification loop
NOTIF -->|push task / warning| APP
APP -->|ack + status| NOTIF
APP -->|confirm arrival via geofence| RULES

%% Escalation & QoD
NOTIF -->|no-ack / SLA breach| SUP
AI -->|optional: enable QoD| QOD

%% Logging
SUB --> AUD
RULES --> AUD
AI --> AUD
NOTIF --> AUD
APP --> AUD
```
