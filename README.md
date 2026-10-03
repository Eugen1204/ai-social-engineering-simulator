# AI Social Engineering Simulator

### Defensive Security Awareness & Social Engineering Simulation Platform

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.139-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=for-the-badge\&logo=sqlalchemy\&logoColor=white)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-pytest-0A9EDC?style=for-the-badge\&logo=pytest\&logoColor=white)](https://pytest.org/)

> 🚧 **Work in Progress**
>
> This project is actively under development. The current version focuses on the core simulation domain, campaign lifecycle, employee interaction tracking, templates, analytics, and risk scoring. AI-powered functionality is part of the project's ongoing development.

---

## Overview

**AI Social Engineering Simulator** is a backend-focused platform for conducting controlled social engineering and phishing-awareness simulations inside an organization.

The system models organizations, departments and employees, allows simulation campaigns to be created and scheduled, tracks employee interactions with simulated messages, and calculates risk metrics based on observed behaviour.

The project is designed as a **defensive security and security-awareness tool** rather than a system for targeting real individuals.

### Core concept

```text
Organization
    │
    ├── Departments
    │       │
    │       └── Employees
    │
    ├── Email Templates
    │
    └── Simulation Campaigns
            │
            ├── Employees
            ├── Events
            ├── Risk Scores
            └── Analytics
```

---

## Current Features

### 🏢 Organization Management

Organizations form the top-level domain entity.

Current functionality includes:

* Create organizations
* Retrieve organizations
* Create departments
* Add employees to departments
* Retrieve employees
* Validate organization data
* Validate employee names and email addresses

Organizations maintain relationships with their departments and employees.

---

### 👥 Employee Management

Employees can be associated with an organization through departments.

The domain model currently tracks:

* Employee identity
* Name
* Email
* Department
* Organization
* Creation timestamp

Employee data is validated through domain value objects.

---

### 📧 Email Templates

The simulator contains a dedicated template domain.

Templates support:

* Creating templates
* Retrieving templates
* Updating templates
* Template versioning
* Rendering template previews
* Variable substitution
* Conditional template sections

Example template syntax:

```text
Hello {{name}},

{% if department %}
This message was prepared for your department.
{% endif %}
```

Templates are rendered using a dedicated template engine rather than directly inside API handlers.

---

### 🎯 Simulation Campaigns

Campaigns represent individual social engineering simulation operations.

A campaign contains:

* Organization
* Email template
* Template version
* Template content snapshot
* Landing page reference
* Assigned employees
* Current lifecycle state

An important design decision is that a campaign stores a **snapshot of the template at creation time**.

This means changes to the original template do not unexpectedly change an already-created campaign.

---

## Campaign Lifecycle

Campaigns use an explicit state machine.

```text
                 ┌─────────────┐
                 │    DRAFT    │
                 └──────┬──────┘
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
       ┌───────────┐          ┌───────────┐
       │ SCHEDULED │─────────▶│  RUNNING  │
       └─────┬─────┘          └─────┬─────┘
             │                      │
             │                      ├──────────────┐
             ▼                      ▼              ▼
       ┌───────────┐          ┌───────────┐  ┌───────────┐
       │ CANCELLED │          │  FINISHED │  │ CANCELLED │
       └───────────┘          └─────┬─────┘  └───────────┘
                                    │
                                    ▼
                              ┌───────────┐
                              │ ARCHIVED  │
                              └───────────┘
```

The current domain model explicitly prevents invalid state transitions.

For example:

* A draft campaign can start immediately.
* A campaign can be scheduled for a future time.
* A scheduled campaign can return to draft.
* A running campaign can be finished or cancelled.
* A finished campaign can be archived.
* Invalid transitions raise domain-specific exceptions.

The lifecycle rules are documented directly in the domain:

`backend/src/social_engineering_simulator/domain/organizations/campaign/CAMPAIGN_LIFECYCLE.md`

---

## Employee Interaction Tracking

The simulation engine tracks individual employee interactions with campaign messages.

Currently supported events include:

* Email sent
* Email opened
* Link clicked
* Credentials submitted

Each interaction is represented in the domain and can generate a corresponding campaign event.

Example:

```text
Email Sent
    │
    ▼
Email Opened
    │
    ▼
Link Clicked
    │
    ▼
Credentials Submitted
```

The domain also prevents logically invalid actions.

For example:

* An email cannot be opened before it is sent.
* A link cannot be clicked before the email is sent.
* Credentials cannot be submitted before the email is opened.

---

## Risk Scoring

Each campaign employee has an individual risk score.

The current scoring model is based on observed campaign behaviour:

| Behaviour             |              Score |
| --------------------- | -----------------: |
| Email sent            |              +0.10 |
| Email opened          |              +0.30 |
| First link click      |              +0.30 |
| Additional clicks     | +0.05 each, capped |
| Credential submission |               1.00 |

The score is capped at `1.0`.

This allows the system to represent an employee's observed susceptibility to the simulated campaign.

---

## Campaign Analytics

The backend provides campaign-level analytics including:

* Total employees
* Sent messages
* Opened messages
* Employees who clicked
* Employees who submitted credentials
* Open rate
* Click rate
* Credential submission rate
* Average risk score
* Number of high-risk employees

The system also exposes individual employee risk profiles and interaction timelines.

---

## Architecture

The backend is structured around separated domain, application, infrastructure and presentation layers.

```text
┌─────────────────────────────────────────────┐
│                 Presentation                │
│                                             │
│ FastAPI • Routers • Schemas • Dependencies  │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                 Application                 │
│                                             │
│ DTOs • Application Services • Use Cases     │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                   Domain                    │
│                                             │
│ Entities • Value Objects • Repositories     │
│ Unit of Work • Domain Rules • State Machine │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                Infrastructure               │
│                                             │
│ PostgreSQL • SQLAlchemy • AsyncPG           │
│ Repository Implementations                  │
└─────────────────────────────────────────────┘
```

The project deliberately keeps domain logic independent from FastAPI and database-specific implementations.

---

## Project Structure

```text
backend/
├── src/
│   └── social_engineering_simulator/
│       │
│       ├── core/
│       │
│       ├── domain/
│       │   ├── organizations/
│       │   │   ├── campaign/
│       │   │   ├── department/
│       │   │   └── ...
│       │   │
│       │   └── email_template/
│       │
│       ├── application/
│       │   ├── dto/
│       │   └── services/
│       │
│       ├── infrastructure/
│       │   └── persistence/
│       │       ├── in_memory/
│       │       └── postgres/
│       │
│       └── presentation/
│           ├── api/
│           │   ├── health.py
│           │   └── v1/
│           │       ├── routers/
│           │       └── schemas/
│           │
│           ├── app.py
│           └── main.py
│
├── migration/
│   └── versions/
│
├── tests/
│   ├── unit/
│   │   ├── application/
│   │   ├── domain/
│   │   └── presentation/
│   │
│   └── integration/
│       └── postgres/
│
├── pyproject.toml
├── uv.lock
└── alembic.ini

docker-compose.yml
.env.example
```

---

## API

The backend is built with **FastAPI**.

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Organizations

```http
POST   /organizations/
GET    /organizations/{organization_id}

POST   /organizations/{organization_id}/employees
GET    /organizations/{organization_id}/employees/{employee_id}
```

### Templates

```http
POST   /organizations/{organization_id}/templates
GET    /organizations/{organization_id}/templates/{template_id}
PATCH  /organizations/{organization_id}/templates/{template_id}

POST   /organizations/{organization_id}/templates/{template_id}/preview
```

### Campaigns

```http
POST   /campaigns/
GET    /campaigns/{campaign_id}

POST   /campaigns/{campaign_id}/start
POST   /campaigns/{campaign_id}/finish
POST   /campaigns/{campaign_id}/cancel
POST   /campaigns/{campaign_id}/schedule

POST   /campaigns/{campaign_id}/employees/{employee_id}
DELETE /campaigns/{campaign_id}/employees/{employee_id}

GET    /campaigns/{campaign_id}/employees/{employee_id}/timeline
GET    /campaigns/{campaign_id}/employees/risk-ranking
GET    /campaigns/{campaign_id}/dashboard
GET    /campaigns/{campaign_id}/employees/{employee_id}/risk-profile
```

FastAPI also provides interactive API documentation through:

```text
/docs
/redoc
```

---

## Persistence

The project currently contains both **in-memory** and **PostgreSQL** persistence implementations.

### PostgreSQL

The PostgreSQL layer uses:

* SQLAlchemy 2.x
* Async SQLAlchemy
* asyncpg
* Repository pattern
* Unit of Work
* SQLAlchemy mappers

The current database model includes:

```text
Organization
    │
    └── Department
            │
            └── Employee
```

Foreign-key constraints and cascading behaviour are defined at the database level where appropriate.

---

## Database Migrations

Database schema changes are managed with **Alembic**.

Migration files are stored under:

```text
backend/migration/versions/
```

---

## Testing

The project contains both unit and integration tests.

Current test coverage is organized around:

### Domain

* Organizations
* Employees
* Campaign statuses
* Campaign lifecycle
* Domain validation

### Application

* Campaign execution
* Scheduling
* Analytics
* Risk scoring
* Campaign events
* Employee risk profiles
* Unit of Work behaviour

### Presentation

* Organization API
* Campaign API
* Template API
* Campaign analytics API
* Campaign events API
* Employee risk profile API

### Integration

* PostgreSQL organization persistence
* Organization → department → employee relationships

Tests are written using **pytest** and **pytest-asyncio**.

---

## Technology Stack

### Backend

* Python 3.13
* FastAPI
* Pydantic
* SQLAlchemy 2.x
* asyncpg
* Alembic
* Uvicorn

### Architecture & Design

* Domain-Driven Design principles
* Repository pattern
* Unit of Work
* Dependency Injection
* Value Objects
* Domain Entities
* Application Services
* State Machine / explicit workflow

### Database

* PostgreSQL 18
* SQLAlchemy AsyncIO
* Alembic

### Testing & Code Quality

* pytest
* pytest-asyncio
* Ruff
* mypy
* pre-commit

### Infrastructure

* Docker
* Docker Compose
* uv

---

## Running Locally

### Requirements

* Python 3.13
* Docker
* Docker Compose
* uv

### 1. Clone the repository

```bash
git clone https://github.com/Eugen1204/ai-social-engineering-simulator.git
cd ai-social-engineering-simulator
```

### 2. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Configure:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=social_engineering_simulator
```

For local development, the PostgreSQL container is exposed on port `5433`.

### 3. Start PostgreSQL

```bash
docker compose up -d postgres
```

### 4. Install backend dependencies

From the `backend` directory:

```bash
cd backend
uv sync
```

### 5. Run migrations

```bash
uv run alembic upgrade head
```

### 6. Start the API

```bash
uv run uvicorn social_engineering_simulator.presentation.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

---

## Development

### Run tests

```bash
uv run pytest
```

### Run linting

```bash
uv run ruff check .
```

### Format code

```bash
uv run ruff format .
```

### Type checking

```bash
uv run mypy src
```

---

## Development Status

🚧 **Active Development**

The current implementation focuses on the core backend and simulation domain.

### Implemented

* Organization management
* Department and employee domain
* Email templates
* Template rendering
* Campaign creation
* Campaign lifecycle
* Campaign scheduling
* Employee assignment
* Simulated email execution
* Email-open events
* Link-click events
* Credential-submission tracking
* Employee risk scoring
* Campaign analytics
* Employee risk profiles
* Employee event timelines
* PostgreSQL persistence
* In-memory persistence
* Unit tests
* PostgreSQL integration tests
* FastAPI API layer

### In Progress

The project is still evolving toward a complete platform, including the higher-level AI-driven simulation capabilities suggested by the project name.

---

## Security & Intended Use

This project is intended for:

* Security-awareness training
* Controlled phishing simulations
* Defensive security research
* Application development and architecture practice
* Measuring employee interaction with simulated security scenarios

The simulator should only be used with **explicit authorization** and within controlled environments.

It is not intended for unauthorized targeting of real individuals or organizations.

---

## Roadmap

The roadmap will evolve together with the project.

Potential areas of development include:

* AI-assisted social engineering scenario generation
* More advanced campaign configuration
* Additional simulated interaction types
* Landing page simulation
* Improved campaign scheduling and execution
* Persistent campaign/event storage
* More detailed analytics
* Improved risk scoring
* Authentication and authorization
* Background task processing
* Production deployment
* Frontend application

---

## Project Status

> **🚧 This project is not production-ready yet.**

The backend is actively being developed and the domain model is still evolving.

The goal is to build a complete platform rather than a simple CRUD application, with emphasis on:

* domain modelling;
* clean separation of responsibilities;
* asynchronous Python;
* reliable persistence;
* testable business logic;
* campaign state management;
* behavioural analytics;
* and eventually AI-assisted simulation workflows.

---

## Author

**Eugen**

Python Backend Developer

[GitHub](https://github.com/Eugen1204)

---

## Repository

[GitHub Repository](https://github.com/Eugen1204/ai-social-engineering-simulator)
