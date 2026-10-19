# ⚡ Learn FASTAPI

### From Python fundamentals to building a real-world backend.

A hands-on journey into backend engineering with **FastAPI, async SQLAlchemy, JWT authentication, and cloud-based media uploads** — learning by building, debugging, and shipping.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=astral&logoColor=white" alt="uv" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
</p>

---

## 🧠 The idea

This repository documents my journey learning backend development by building things that actually work.

Instead of collecting tutorials, I'm exploring how backend systems fit together — from HTTP requests and database models to authentication, file uploads, and API design.

The goal: **understand the system, not just make the code run.**

## ✨ What's inside

- 🚀 **FastAPI** — building API endpoints and handling requests.
- 🔐 **Authentication** — registration, login, JWT-based authentication, and protected routes using FastAPI Users.
- 🗄️ **Database & ORM** — SQLAlchemy models, async database sessions, and relationships between users and posts.
- 🖼️ **Media uploads** — uploading images and videos through ImageKit.
- 📰 **Social media feed** — retrieving posts, identifying post owners, and returning feed data.
- 🧹 **CRUD operations** — creating, reading, and deleting posts.
- ⚡ **Async Python** — asynchronous database operations and offloading blocking upload calls.
- 📦 **Modern Python tooling** — dependency and environment management with `uv`.

## 🛠️ Tech stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| FastAPI | API framework |
| SQLAlchemy | ORM and database interactions |
| SQLite + aiosqlite | Local database and async driver |
| FastAPI Users | User management and authentication |
| JWT | Bearer-token authentication |
| ImageKit | Cloud media storage |
| Pydantic | Data validation and schemas |
| uv | Python project and dependency management |

## 🚦 Getting started

### Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- An [ImageKit](https://imagekit.io/) account for media uploads

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd "Learn FASTAPI"
```

### 2. Install dependencies

Install `uv` using its [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

Then install the project's dependencies:

```bash
uv sync
```

This creates the project's virtual environment and installs dependencies defined in `pyproject.toml`, using `uv.lock` when available.

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
IMAGEKIT_PRIVATE_KEY=your_imagekit_private_key
SECRET=your_random_secret
```

Generate a strong, random secret for authentication. Never commit `.env` or real credentials to Git.

### 4. Run the server

From the project root:

```bash
uv run uvicorn app.app_db:server --reload
```

This command assumes your FastAPI instance is named `server` in `app/app_db.py`.

### 5. Explore the API

Once the server is running:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Use the interactive documentation to inspect endpoints, register a user, authenticate, and test protected operations.

## 🔌 API overview

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Welcome response |
| `POST` | `/auth/register` | Register a user |
| `POST` | `/auth/jwt/login` | Log in and obtain a token |
| `GET` | `/feed` | Retrieve the post feed |
| `POST` | `/upload` | Upload media and create a post |
| `DELETE` | `/posts/{post_id}` | Delete a post you own |

Authentication routes are provided by FastAPI Users. Protected endpoints require a valid bearer token.

For exact request formats and the complete list of available routes, check `/docs`.

## 🗺️ Learning roadmap

- [x] Build API endpoints with FastAPI
- [x] Model users and posts with SQLAlchemy
- [x] Connect asynchronous database sessions
- [x] Implement JWT-based authentication
- [x] Associate posts with their owners
- [x] Upload media to ImageKit
- [x] Implement a user-aware feed
- [x] Add ownership checks for post deletion
- [ ] Add automated tests
- [ ] Add database migrations
- [ ] Build a frontend
- [ ] Containerize and deploy

*The roadmap reflects the current learning direction; check the code for the latest implementation status.*

## ⚡ Why uv?

This project uses [`uv`](https://docs.astral.sh/uv/) for Python dependency and environment management.

- ⚡ Fast dependency installation and resolution
- 🔒 Reproducible environments with a lockfile
- 🧰 Automatic virtual environment management
- 🐍 Convenient Python project management

**Recommendation:** If you're starting a Python project, give `uv` a try.

## 🔒 Security notes

- Keep `.env` out of version control.
- Use strong, randomly generated secrets.
- Validate uploaded file types and sizes.
- Keep private credentials on the backend.
- Enforce authentication and resource ownership on protected operations.

## 🤝 Contributing

This is a learning-focused project, and constructive feedback is welcome.

Found a bug or have an improvement in mind? Open an issue or submit a pull request.

## ⭐ Follow the journey

If you're learning FastAPI or exploring backend engineering too, feel free to explore the code, share feedback, and star the repository if you find it useful.

**Learn by building. Debug by understanding. Ship by iterating.**

---

<p align="center">
  <sub>Built with Python ☕ and a lot of debugging.</sub>
</p>