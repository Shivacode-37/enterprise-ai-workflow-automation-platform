# Enterprise AI Workflow Automation Platform

An AI-assisted IT asset request and approval platform built with
 **FastAPI** ,  **Streamlit** ,  **PostgreSQL** ,  **SQLAlchemy** ,
 **LangChain** ,  **LangGraph** , and  **Chroma** .

The application lets an employee describe an IT asset need in natural
language, analyzes the request with an AI workflow and policy knowledge,
routes it for approval, and records workflow outcomes and audit events.

> **Project status:** Core workflows and the dashboard are implemented.
> End-to-end verification and deployment are the next steps. Review the
> current code and environment configuration before deploying.

## Highlights

* AI-assisted asset requests from natural-language descriptions.
* Policy-aware analysis using a local knowledge file and vector
  retrieval.
* LangGraph workflow for analysis and validation.
* Approval workflow before asset allocation.
* Inventory tracking and available-asset allocation.
* Workflow-run monitoring and audit-event history.
* Streamlit dashboard with Overview, Create AI Request, Asset
  Requests, Approvals, Inventory, Workflow Runs, and Audit Logs pages.
* Dark and Light appearance options.

## Architecture

```
Employee
   |
   v
Streamlit Dashboard
   | HTTP requests
   v
FastAPI REST API
   +--> LangChain / LangGraph AI analysis
   |       +--> Policy knowledge file / Chroma
   +--> Requests and approvals
   +--> Inventory allocation
   +--> Workflow runs and audit logs
   |
   v
PostgreSQL
```

The frontend and backend are separate processes in local development.
The dashboard calls FastAPI using `API_BASE_URL`; both processes must be
running locally unless the dashboard points to a deployed API.

## Technology stack

Python, FastAPI, Uvicorn, Streamlit, SQLAlchemy, PostgreSQL, Docker,
LangChain, LangGraph, Chroma, Pydantic, Requests, and JWT-based
authentication components.

## Repository structure

```
enterprise-ai-workflow-automation-platform/
├── app/
│   ├── api/routes/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── knowledge/
├── frontend/
│   └── dashboard.py
├── scripts/
│   └── seed_inventory.py
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── .gitignore
└── README.md
```

Actual files may vary; check the current repository before relying on
this illustrative tree.

## Prerequisites

* Python version supported by the project's dependencies
* PostgreSQL locally or in Docker
* Git
* An OpenAI API key if the current AI analysis implementation calls
  OpenAI
* Docker Desktop for the Docker-based database setup

## Local setup

### 1. Clone the repository

```
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd enterprise-ai-workflow-automation-platform
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If `requirements.txt` exists:

```
pip install -r requirements.txt
```

Before deployment, ensure the dependency file exists, is complete, and
has been tested in a clean environment.

### 4. Configure environment variables

Create a local `.env` file using the exact variable names expected by
the current code. Common examples for this stack are:

```
OPENAI_API_KEY=replace_with_your_key
JWT_SECRET_KEY=replace_with_a_long_random_secret
DATABASE_URL=replace_with_your_database_connection_string
```

These are examples, not a guarantee of the exact names used by the
current code. Check the settings in `app/` and your existing environment
configuration. Never commit `.env`, API keys, database passwords, or JWT
secrets.

### 5. Start PostgreSQL

If your existing database container is named `enterprise_ai_postgres`:

```
docker start enterprise_ai_postgres
```

If it does not exist, use the project's existing database configuration
or create a container with the database name, credentials, and port
expected by the app. Check the existing setup before creating another
database container.

### 6. Start FastAPI

From the project root:

```
uvicorn app.main:app --reload
```

* API: `http://127.0.0.1:8000`
* Swagger: `http://127.0.0.1:8000/docs`

### 7. Start Streamlit

Open a second terminal, activate the virtual environment, and run:

```
streamlit run frontend/dashboard.py
```

Open `http://localhost:8501`.

The dashboard currently uses `API_BASE_URL`, which defaults to
`http://127.0.0.1:8000` in the application code. For deployment,
configure it to use the public HTTPS URL of the FastAPI service.

## Typical workflow

1. Submit an IT asset request in natural language.
2. The AI analysis flow extracts structured request information and
   consults the policy knowledge source.
3. The application creates a request and pending approval.
4. An approver approves or rejects the request.
5. An approved request triggers the asset-allocation workflow.
6. The workflow records its outcome and audit events.
7. Review the request, inventory, workflow run, and audit log in the
   dashboard.

Actual outcomes depend on the current database, available inventory, AI
provider configuration, and validation rules.

## API exploration

Start FastAPI and visit `http://127.0.0.1:8000/docs` to inspect the
exact routes and schemas implemented in the current code. Routes include
asset management, AI requests, approvals, workflow runs, audit logs, and
authentication.

## Deployment roadmap

1. Verify the full request-to-audit workflow locally.
2. Confirm `requirements.txt`, `.gitignore`, environment variables, and
   database initialization.
3. Create a backend Docker image and a separate Streamlit frontend
   image.
4. Use Docker Compose to run the frontend, backend, and PostgreSQL
   together for local development.
5. Deploy PostgreSQL to a managed database service for production.
6. Deploy FastAPI as a web service and configure secrets plus
   `DATABASE_URL`.
7. Deploy Streamlit and set `API_BASE_URL` to the FastAPI public HTTPS
   URL.
8. Test production connectivity, persistence, AI API access,
   authentication, logs, and failure cases.

Deploying Streamlit alone does not automatically start the separate
FastAPI process or PostgreSQL database. They must be deployed as
separate services or explicitly orchestrated together.

## Production security checklist

* Keep `.env` and credentials out of Git.
* Use strong production secrets and rotate exposed keys.
* Use HTTPS for public traffic.
* Restrict database network access and use secure credentials.
* Verify authentication and authorization on every sensitive endpoint;
  having a login endpoint does not by itself secure all business
  routes.
* Configure CORS only if needed and only for trusted frontend origins.
* Review request limits, timeouts, logging, and error handling.
* Ensure database initialization or migrations are repeatable.
* Test rejection, successful allocation, unavailable inventory, and
  AI/API failure paths.
* Do not claim production readiness until these checks are complete.

## Testing checklist

* [ ] FastAPI starts and `/docs` loads.
* [ ] Streamlit connects to FastAPI.
* [ ] Inventory data and filters work.
* [ ] An AI request creates the expected request and approval.
* [ ] Approval and rejection paths work.
* [ ] Approved requests allocate available inventory.
* [ ] Unavailable inventory produces a clear failure outcome.
* [ ] Workflow runs and audit events reflect outcomes.
* [ ] Dark and Light themes remain readable.
* [ ] Secrets are excluded from Git.
* [ ] Deployed frontend reaches the deployed backend.
