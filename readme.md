flowchart LR
subgraph EA[External App: Festival/Event Platform]
Admin[Admin UI: StageFlow Web]
DB[(Database)]
StaffApp[Staff Mobile App]
end

subgraph Nokia[Nokia Network as Code]
Loc[Location API / Location Verification]
Geo[Geofencing API (optional)]
QoD[Quality on Demand API]
end

Admin -->|Create event, zones, roles| DB
Admin -->|Assign users to roles/groups| DB

StaffApp -->|Login / get profile| DB
StaffApp -->|Periodic location signal or trigger check| Admin

Admin -->|Verify location| Loc
Admin -->|Optional zone membership| Geo

Admin -->|If user role eligible AND inside zone| QoD
QoD -->|Priority connectivity policy applied| Telco[(Operator Network)]

Telco --> Users[General crowd users]
Telco --> StaffOnly[Staff users with QoD]

Admin -->|Audit logs: who/when/where| DB
StaffApp <-->|Status: QoD ON/OFF, zone, tasks| Admin