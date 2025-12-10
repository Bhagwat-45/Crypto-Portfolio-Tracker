# 📈 Crypto Portfolio Tracker

A real-time, asynchronous backend service built with **FastAPI** and **PostgreSQL** to track the value and Profit & Loss (P&L) of a user's cryptocurrency portfolio by periodically fetching price data from external APIs.

## ✨ Key Features

* **Asynchronous Data Ingestion:** Uses a background worker to periodically pull the latest market prices for tracked assets (e.g., BTC, ETH) from an external API (e.g., CoinGecko).
* **Time-Series Storage:** Stores historical price data using SQLAlchemy to enable tracking of trends and performance over time.
* **Portfolio Management:** REST endpoints to add, view, and update owned assets (quantity and average buy price).
* **Real-Time Analytics:** Calculates current portfolio value and Profit & Loss (P&L) based on the latest price snapshots.

## 🏛️ Technical Architecture

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Framework** | **FastAPI** (Python) | High-performance, asynchronous request handling. |
| **Database** | **PostgreSQL** | Persistent storage for assets and price history. |
| **ORM** | **SQLAlchemy** (Async) | Handling all database interactions. |
| **Migrations** | **Alembic** | Database schema version control. |
| **Data Source** | `httpx` / External API | Asynchronous fetching of real-time price data. |
| **Scheduling** | **FastAPI Background Tasks** / Polling Logic | Periodic execution of the price fetching worker. |

## 📦 Data Model Overview

The core data is stored across two related tables:

1.  **`Asset`**: What the user owns (`symbol`, `quantity`, `average_buy_price`).
2.  **`PriceSnapshot`**: Time-series price data (`asset_id`, `timestamp`, `price`).



## 🛠️ Installation & Setup

### Prerequisites

* Python 3.10+
* PostgreSQL
* Virtual environment (recommended)

### Local Development

1.  **Clone the Repository:**
    ```bash
    git clone <Your-Repo-Link>
    cd crypto-portfolio-tracker
    ```

2.  **Setup Environment:**
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration (.env):**
    Create a `.env` file in the root directory and configure your database and API key:

    ```ini
    # Database Configuration
    DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/crypto_db
    
    # External API Key (e.g., CoinGecko or another data source)
    CRYPTO_API_BASE_URL=[https://api.coingecko.com/api/v3](https://api.coingecko.com/api/v3)
    ```

5.  **Run Database Migrations (Alembic):**
    ```bash
    alembic upgrade head
    ```

6.  **Start the Server:**
    ```bash
    uvicorn app.main:app --reload
    ```

## 🔌 API Endpoints

The interactive Swagger documentation will be available at `http://127.0.0.1:8000/docs`.

### Portfolio Management

* `POST /api/assets/`: Add a new asset holding (e.g., {"symbol": "BTC", "quantity": 0.5, "average_buy_price": 40000}).
* `GET /api/assets/`: Retrieve a list of all assets in the portfolio.
* `GET /api/assets/{symbol}`: Retrieve details and the latest P&L for a specific asset.

### Analytics

* `GET /api/analytics/portfolio_summary`: Get total portfolio value, total P&L, and overall performance metrics.
* `GET /api/analytics/historical_prices/{symbol}`: Retrieve time-series price data for charting.

## 🤝 Contribution

Feel free to open issues or submit pull requests.

## 📄 License

This project is licensed under the MIT License.