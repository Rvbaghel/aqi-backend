# 🌍 SkyGuard - Air Quality Intelligence Platform (Backend)

<div align="center">

[![SkyGuard](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://skyguard-aqi.streamlit.app)

**High-performance REST API for real-time air quality monitoring**


</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

SkyGuard Backend is a robust FastAPI-based REST API that powers the SkyGuard air quality monitoring platform. It fetches real-time AQI data from government APIs, stores it in a PostgreSQL database (hosted on Neon), and provides efficient endpoints for the frontend application.

### Key Capabilities

- **Real-Time Data Fetching**: Automated AQI data collection from monitoring stations
- **Efficient Caching**: Optimized database queries with intelligent caching
- **RESTful API**: Clean, documented endpoints following REST principles
- **Scheduled Jobs**: Automated data updates using APScheduler
- **Scalable Architecture**: Designed for horizontal scaling on Render

---

## ✨ Features

### 🔄 Core Functionality
- **Automated Data Collection**: Scheduled fetching of AQI data every 30 minutes
- **Multi-City Support**: Monitoring 6+ major Indian cities
- **Historical Data**: 24-hour historical AQI tracking
- **Health Recommendations**: Dynamic health advice based on AQI levels

### 🚀 API Features
- **Fast Response Times**: Optimized queries with connection pooling
- **CORS Support**: Configured for frontend integration
- **Error Handling**: Comprehensive error responses
- **Input Validation**: Pydantic models for request/response validation
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

### 💾 Database Features
- **PostgreSQL on Neon**: Serverless database with automatic scaling
- **Connection Pooling**: Efficient connection management
- **Data Persistence**: Reliable storage with ACID compliance
- **Indexing**: Optimized queries with proper indexes

---

## 🛠️ Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **FastAPI** | Web framework | 0.104+ |
| **PostgreSQL** | Database (Neon) | 14+ |
| **SQLAlchemy** | ORM | 2.0+ |
| **Psycopg2** | PostgreSQL adapter | 2.9+ |
| **APScheduler** | Task scheduling | 3.10+ |
| **Uvicorn** | ASGI server | 0.24+ |
| **Pydantic** | Data validation | 2.0+ |
| **Python-dotenv** | Environment management | 1.0+ |
| **Requests** | HTTP client | 2.31+ |

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Government │      │   SkyGuard   │      │  Frontend   │
│  AQI APIs   │─────▶│   Backend    │◀─────│  (Streamlit)│
│             │      │   (FastAPI)  │      │             │
└─────────────┘      └──────┬───────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  PostgreSQL  │
                     │  (Neon DB)   │
                     └──────────────┘

Flow:
1. APScheduler triggers data fetch every 30 minutes
2. Backend fetches AQI data from government APIs
3. Data processed and stored in PostgreSQL
4. Frontend requests data via REST endpoints
5. Backend retrieves from database and responds
```

### Component Breakdown

- **Routers**: Handle HTTP requests and route to appropriate handlers
- **Services**: Business logic for data fetching and processing
- **Database Layer**: SQLAlchemy models and connection management
- **Scheduler**: Background jobs for automated data collection
- **Core**: Configuration, utilities, and shared resources

---

## 📁 Project Structure

```
project-root/
│
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore rules
│
├── app/
│   ├── __init__.py             # App initialization
│   │
│   ├── routers/                # API route handlers
│   │   ├── __init__.py
│   │   ├── aqi.py             # AQI endpoints
│   │   ├── cities.py          # City endpoints
│   │   └── health.py          # Health recommendation endpoints
│   │
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   └── scheduler.py       # Background job scheduler
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   └── aqi_fetcher.py     # Data fetching service
│   │
│   └── db/                     # Database layer
│       ├── __init__.py
│       ├── database.py        # DB connection and session
│       └── models.py          # SQLAlchemy models
│
└── README.md                   # This file
```

---

#### 🏥 Health Recommendations

**GET** `/api/health/{aqi}`
- **Description**: Get health recommendations based on AQI level
- **Parameters**:
  - `aqi` (path): AQI level (1-5)
- **Response**:
  ```json
  {
    "aqi": 3,
    "level": "Moderate",
    "color": "#eab308",
    "safe_window": "1 - 2 Hours",
    "recommendations": [
      "Sensitive groups should wear masks",
      "Reduce heavy outdoor exertion"
    ]
  }
  ```

### Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting for production use.

---

## 🚢 Deployment

### Deploying to Render


### Neon Database Setup


### Health Checks

Add a health check endpoint:

```python
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

---

## 📊 Monitoring

## 🤝 Contributing

Contributions welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Contact

**Vishal Baghel**
- Email: baghelvishal264@gmail.com
- LinkedIn: [vishal-baghel-a055b5249](https://www.linkedin.com/in/vishal-baghel-a055b5249/)
- GitHub: [@VISHAL BAGHEl](https://github.com/Rvbaghel)

**Project Links**
- WEBAPPLICATION LINK: [https://skyguard-aqi.streamlit.app/](https://skyguard-aqi.streamlit.app/)
---

## 🙏 Acknowledgments

- FastAPI for the excellent framework
- Neon for serverless PostgreSQL
- Render for reliable hosting
- Government AQI monitoring stations for data

---

<div align="center">

**Built with ❤️ by Vishal Baghel**

**SkyGuard Systems © 2025 - v2.5.0 Stable Release**

</div>

