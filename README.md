# Personal Finance Auditor API

A Django REST Framework API for recording personal financial transactions and performing basic financial auditing and analysis.

The project provides transaction management and audit-focused insight endpoints for identifying spending patterns, large transactions, duplicate transactions, unusual activity, and summary information.

## Features

- Create, view, update, and delete financial transactions
- Categorize transactions by income and expense categories
- Analyze transaction insights
- Analyze spending by category
- Identify potential audit alerts
- Detect large transactions
- Detect duplicate transactions
- Identify unusual transactions
- Generate an audit summary
- Interactive Swagger API documentation
- Automated API tests

## Technologies Used

- Python
- Django
- Django REST Framework
- drf-spectacular
- SQLite
- Swagger / OpenAPI
- Git & GitHub

## API Endpoints

### Transactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/transactions/` | List transactions |
| POST | `/api/transactions/` | Create a transaction |
| GET | `/api/transactions/{id}/` | Retrieve a transaction |
| PUT | `/api/transactions/{id}/` | Update a transaction |
| PATCH | `/api/transactions/{id}/` | Partially update a transaction |
| DELETE | `/api/transactions/{id}/` | Delete a transaction |

### Audit & Insights

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/insights/` | View financial insights |
| GET | `/api/insights/categories/` | Analyze transactions by category |
| GET | `/api/insights/alerts/` | View audit alerts |
| GET | `/api/insights/large-transactions/` | Identify large transactions |
| GET | `/api/insights/duplicates/` | Identify duplicate transactions |
| GET | `/api/insights/unusual/` | Identify unusual transactions |
| GET | `/api/insights/summary/` | View audit summary |

## API Documentation

The API includes interactive Swagger documentation powered by `drf-spectacular`.

When the development server is running, open:

http://127.0.0.1:8000/api/docs/

The OpenAPI schema is available at:

http://127.0.0.1:8000/api/schema/

The Swagger interface allows the available API endpoints and request/response structures to be explored directly from the browser.

## Example Transaction

### Request

```json
{
    "transaction_type": "expense",
    "amount": "3000.00",
    "category": "food",
    "description": "Lunch",
    "transaction_date": "2026-08-30"
}
```

### Response

```json
{
    "id": 7,
    "transaction_type": "expense",
    "amount": "3000.00",
    "category": "food",
    "description": "Lunch",
    "transaction_date": "2026-08-30",
    "created_at": "2026-08-30T18:11:39.774158Z",
    "updated_at": "2026-08-30T18:11:39.774188Z"
}
```

## Project Structure

```text
personal-finance-auditor-api/
│
├── audits/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .gitignore
├── manage.py
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Samito3011/personal-finance-auditor-api.git
```

Navigate into the project:

```bash
cd personal-finance-auditor-api
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install django djangorestframework drf-spectacular
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at:

http://127.0.0.1:8000/

## Running Tests

The project includes automated tests for the audit functionality.

Run:

```bash
python manage.py test audits
```

Current test result:

```text
Found 5 test(s).

.....

Ran 5 tests

OK
```

## Purpose

This project was developed as a backend portfolio project to demonstrate practical experience with:

- REST API development
- Django and Django REST Framework
- CRUD operations
- Data validation and serialization
- Financial transaction processing
- Audit-oriented data analysis
- Automated API testing
- API documentation with OpenAPI and Swagger
- Git version control and GitHub

## Author

**Samito3011**

GitHub:

https://github.com/Samito3011