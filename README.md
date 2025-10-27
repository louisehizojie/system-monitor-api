# 🐍 System Monitor API (FastAPI)

A feature-rich, minimalist backend API built with **FastAPI** to serve real-time system metrics. This project is designed as an advanced starting template for Python and FastAPI developers, offering solutions for production-ready concerns like service management, security, and logging right out of the box.

## ✨ Features & Starter Packs

* **⚡️ High Performance:** Built on FastAPI for speed and asynchronous operations.
* **🔒 Security Best Practices:** Includes templates for securing API endpoints with JSON Web Tokens.
* **🛠️ System Service Ready:** Includes configuration files and scripts to easily run the application as a **Windows Service**.
* **✅ SSL/TLS Enabled:** Configuration templates for running the server with **SSL/TLS** encryption.
* **📄 Configuration Management:** Reads application settings from a simple **YAML configuration file**.
* **📊 Advanced Logging:** Integrates **Loguru** for simple, yet powerful logging (rotation, file management, and clean output).
* **🔍 System Checks:**
    * Check the operational status of local **Windows Services**.
    * Monitor the availability of external **Web APIs** and **Web Applications**.
* **💾 Database Integration:** Includes a working example for connecting and making simple calls to an **Oracle Database**.

---

## 🚀 Getting Started

These instructions will get a copy of the project up and running on your local machine.

### Prerequisites

You'll need **Python 3.8+** and a package manager like `pip`.

* **Python** (LTS version recommended)
* **pip**

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/louisehizojie/system-monitor-api.git](https://github.com/louisehizojie/system-monitor-api.git)
    cd YOUR_FASTAPI_REPO_NAME
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    .\venv\Scripts\activate   # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ⚙️ Configuration

All core settings for the application are managed in the **`config/config.yaml`** file.

### Key Settings:

| Parameter | Location | Description |
| :--- | :--- | :--- |
| `SERVER_INFO` | `config.yaml` | Controls the Uvicorn binding address. |
| `LOGGING` | `config.yaml` | Loguru configuration (level, file path, rotation). |
| `JWT_INFO` | `config.yaml` | JWT Token configuration (secret, algorithm, expiry). |
| `DB_CONN_INFO` | `config.yaml` | Connection details for the Oracle database. |

**Always review and update the `config.yaml` with your own environment details before running.**

---

## 🏃 Running the API

### 1. Simple Local Development

Run the API using Uvicorn. The default port is `8000`.

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --ssl-keyfile cert/private_key_sample.pem --ssl-certfile cert/public_certificate_sample.pem

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Contact
Louis Ehizojie - [Github](https://github.com/louisehizojie)