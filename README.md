# final_Hackthon
This Class Contains a Real Time Data
# 🚀 On-Premise IoT Data Migration to AWS Cloud

> A complete end-to-end Data Engineering project that simulates an on-premise IoT environment and migrates streaming data to AWS Cloud for real-time analytics using Kafka, Snowflake, dbt, Streamlit, and Grafana.

![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazon-aws)
![Kafka](https://img.shields.io/badge/Apache-Kafka-black?logo=apache-kafka)
![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Cloud-blue?logo=snowflake)
![dbt](https://img.shields.io/badge/dbt-Transformations-orange?logo=dbt)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Grafana](https://img.shields.io/badge/Grafana-Visualization-orange?logo=grafana)

---

# 📖 Project Overview

This project demonstrates a **real-world enterprise data engineering pipeline** where IoT devices continuously generate telemetry and geolocation data from an on-premise environment.

The objective is to migrate streaming sensor data from an on-premise PostgreSQL database to AWS Cloud using modern data engineering tools and best practices.

The project is divided into two major phases:

### 🔹 Phase 1 — Data Ingestion

- Simulate IoT devices
- Publish MQTT messages to AWS IoT Core
- Stream events into Apache Kafka (AWS MSK)
- Store events inside PostgreSQL
- Backup data to Amazon S3

### 🔹 Phase 2 — Data Migration & Analytics

- Capture database changes using Debezium CDC
- Stream CDC events into Snowflake
- Transform data using dbt
- Build analytical dashboards using Streamlit
- Visualize time-series data in Grafana

---

# 🏗 Solution Architecture

```
IoT Sensors (Simulated)
        │
      MQTT
        │
        ▼
AWS IoT Core
        │
        ▼
Apache Kafka (AWS MSK)
       │
 ┌─────┴────────────┐
 │                  │
 ▼                  ▼
Kafka JDBC      Kafka S3
 Sink            Backup
 │                  │
 ▼                  ▼
PostgreSQL        Amazon S3
 (EC2)
 │
 ▼
Debezium CDC
 │
 ▼
Kafka MSK
 │
 ▼
Snowflake
(Bronze Layer)
 │
 ▼
dbt
 │
 ├────────► Silver Layer
 │
 └────────► Gold Layer
                 │
        ┌────────┴─────────┐
        ▼                  ▼
  Streamlit          AWS Timestream
 Dashboard                 │
                            ▼
                        Grafana
```

---

# ⚙️ Technology Stack

| Category | Technologies |
|-----------|--------------|
| Cloud | AWS |
| Infrastructure | AWS CDK (Python) |
| Streaming | Apache Kafka (AWS MSK) |
| Messaging | MQTT |
| IoT | AWS IoT Core |
| Database | PostgreSQL |
| CDC | Debezium |
| Data Warehouse | Snowflake |
| Data Modeling | dbt |
| Programming | Python |
| Dashboard | Streamlit |
| Visualization | Grafana |
| Backup | Amazon S3 |
| Time-Series | AWS Timestream |

---

# 📂 Repository Structure

```text
.
├── cdk/
├── kafka-connect/
├── iot-simulator/
├── dbt/
├── streamlit/
├── lambda/
├── grafana/
├── docs/
└── README.md
```

---

# 📊 Data Pipeline

## Phase 1 — IoT Data Ingestion

```
IoT Devices
      │
      ▼
AWS IoT Core
      │
      ▼
Kafka (AWS MSK)
      │
      ▼
Kafka Connect
      │
      ▼
PostgreSQL (EC2)
      │
      └──────────────► Amazon S3 Backup
```

---

## Phase 2 — Cloud Migration & Analytics

```
PostgreSQL
      │
      ▼
Debezium CDC
      │
      ▼
Kafka
      │
      ▼
Snowflake
(Bronze)
      │
      ▼
dbt
      │
      ├────────► Silver
      │
      └────────► Gold
                    │
        ┌───────────┴──────────┐
        ▼                      ▼
   Streamlit Dashboard     AWS Timestream
                                   │
                                   ▼
                               Grafana
```

---

# ✨ Features

- ✅ Simulated IoT sensor data
- ✅ MQTT communication
- ✅ Apache Kafka streaming
- ✅ AWS MSK integration
- ✅ PostgreSQL on EC2
- ✅ Kafka Connect JDBC Sink
- ✅ Amazon S3 backup
- ✅ Debezium Change Data Capture (CDC)
- ✅ Snowflake Data Warehouse
- ✅ dbt Bronze → Silver → Gold transformations
- ✅ Streamlit Dashboard
- ✅ AWS Timestream
- ✅ Grafana Monitoring
- ✅ Infrastructure as Code using AWS CDK

---

# 🚀 Getting Started

## Prerequisites

- AWS Account
- AWS CLI
- Python 3.10+
- Node.js
- Docker
- Snowflake Account
- Git

---

## Clone Repository

```bash
git clone https://github.com/yourusername/your-repository.git

cd your-repository
```

---

# 🛠 Deploy Infrastructure

```bash
cd cdk

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

cdk bootstrap

cdk deploy
```

---

# ▶ Run IoT Simulation

Deploy the AWS IoT Device Simulator and import the provided device template.

Start multiple virtual devices and verify that MQTT messages are reaching Kafka.

---

# 🔄 Configure Kafka Connect

```bash
curl -X POST \
-H "Content-Type: application/json" \
--data @kafka-connect/jdbc-sink-connector.json \
http://localhost:8083/connectors
```

---

# 🔁 Configure Debezium CDC

```bash
curl -X POST \
-H "Content-Type: application/json" \
--data @kafka-connect/debezium-postgres-source.json \
http://localhost:8083/connectors
```

---

# ❄️ Configure Snowflake Connector

```bash
curl -X POST \
-H "Content-Type: application/json" \
--data @kafka-connect/snowflake-sink-connector.json \
http://localhost:8083/connectors
```

---

# 📈 Run dbt Models

```bash
cd dbt

dbt run

dbt test

dbt docs generate

dbt docs serve
```

---

# 📊 Launch Dashboard

```bash
cd streamlit

pip install -r requirements.txt

streamlit run app.py
```

---

# 📸 Screenshots

Add screenshots inside:

```
docs/screenshots/
```

Example:

- AWS IoT Core
- Kafka MSK
- PostgreSQL
- Snowflake
- dbt Lineage
- Streamlit Dashboard
- Grafana Dashboard

---

# 📁 Project Deliverables

- AWS CDK Infrastructure
- Kafka Connect Configuration
- Debezium CDC
- Snowflake Integration
- dbt Models
- Streamlit Dashboard
- Grafana Dashboard
- Documentation
- Architecture Diagram

---

# 📌 Project Workflow

```
IoT Sensors
      │
      ▼
AWS IoT Core
      │
      ▼
Kafka MSK
      │
      ▼
PostgreSQL
      │
      ▼
Debezium CDC
      │
      ▼
Snowflake
      │
      ▼
dbt
      │
      ▼
Analytics
      │
 ┌────┴────┐
 ▼         ▼
Streamlit Grafana
```

---

# 👨‍💻 Author

**Muhammad Ali**

Data Engineering Hackathon — Batch 03

---

# 🙏 Acknowledgements

Special thanks to **Qasim Hassan** for designing and mentoring this Data Engineering Hackathon project.

---

# 📜 License

This project is intended for educational purposes as part of the Data Engineering Hackathon.

