# Address Book API

FastAPI-based Address Book application.

## Features

- Create address
- Get all addresses
- Update address
- Delete address
- Find nearby addresses using coordinates and distance
- SQLite database
- Swagger API documentation

---

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Geopy

---

## Installation

### Clone repository

```bash
git clone <your-repository-url>
```

### Create virtual environment

```bash
python -m venv .venv
```

### Activate virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run application

```bash
uvicorn app.main:app --reload
```

---

## Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /addresses/ | Create address |
| GET | /addresses/ | Get all addresses |
| PUT | /addresses/{id} | Update address |
| DELETE | /addresses/{id} | Delete address |
| GET | /addresses/nearby/ | Find nearby addresses |
