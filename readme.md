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
1. ** Staff control


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
