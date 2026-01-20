# Litestar Product Service
This is a REST API for a product invenroty management aplication built to demonstrate [Litestar](https://litestar.dev/), a modern opinionated ASGI web framework for building web applications in Python.

## Install Requirements 
```bash
$ uv sync
```

## Run the application

```bash
$ uv run litestar --app main:app run -rd
```

Full project was part of a podcast series [here](https://youtube.com/playlist?list=PLEt8Tae2spYncMXg-YJZfjk5Ls2PfQOBS&si=E4leZS8-OhVct5hZ)

## Remaining Topics

## High Priority (Next 3–5 Videos – Core & Most Requested Features)
- [ ] **Video #6: Dependency Injection Deep Dive**  
  - Explain Litestar's powerful DI system (request-scoped, app-scoped, stateful/stateless)  
  - Refactor existing CRUD repo/service to use injected dependencies  
  - Inject DB session, current user, config, etc.  
  - Why it's better than manual passing in many frameworks

- [ ] **Video #7: DTOs (Data Transfer Objects) for Safe & Clean APIs**  
  - Intro to Litestar DTO system (DTOConfig, DataclassDTO, partial updates)  
  - Create read/write DTOs for your models to control exposed fields  
  - Prevent over-posting/mass assignment issues  
  - Update CRUD endpoints to use DTOs

- [ ] **Video #8: Authentication with JWT & Guards**  
  - Set up JWT auth (using litestar[jwt] extra)  
  - Implement login/register endpoints  
  - Use guards to protect routes  
  - Inject current_user via dependency  
  - Add role-based access (e.g., admin-only delete)

- [ ] **Video #9: Error Handling & Problem Details**  
  - Custom exceptions & global handlers  
  - Built-in RFC 7807 Problem Details support  
  - Validation/business error responses  
  - Improve UX for your API consumers

## Medium Priority (Production Essentials)
- [ ] **Video #10: Testing Litestar Apps**  
  - Use litestar.testing (TestClient, create_test_app)  
  - Test routes, dependencies, DB (with pytest + pytest-databases?)  
  - Mock dependencies & test async code

- [ ] **Video #11: WebSockets for Real-Time Features**  
  - Set up WebSocket listeners & basic connection handling  
  - Simple example: live updates when a TODO/CRUD item changes  
  - Show serialization with msgspec

- [ ] **Video #12: Caching & Stores (Redis/Valkey)**  
  - Use Litestar's stores framework  
  - Response caching for expensive endpoints  
  - Cache DB queries in your CRUD app

- [ ] **Video #13: Middleware, Compression & Lifecycle Hooks**  
  - Custom middleware (logging, CORS, rate limiting)  
  - Enable Brotli compression  
  - App/request/response hooks

## Lower Priority / Bonus Videos (Advanced & Fun)
- [ ] **Video #14: Observability – Metrics & Logging**  
  - Prometheus/OpenTelemetry integration  
  - Structured logging with structlog  
  - Monitor your running API

- [ ] **Video #15: Deployment – Docker + Production Server**  
  - Dockerize the app  
  - Run with Gunicorn + Uvicorn workers  
  - Tips for Render, Fly.io, Railway, etc.

- [ ] **Video #16: Templating + HTMX (Server-Side Rendering)**  
  - Jinja2 templates  
  - HTMX plugin/integration for interactive UI without heavy frontend  
  - Simple frontend on top of your API

- [ ] **Video #17: Project Structure & Best Practices**  
  - Clean folder layout (controllers, dtos, services, repositories)  
  - Config with pydantic-settings/env vars  
  - Scaling to larger apps

- [ ] **Video #18: Comparison – Litestar vs FastAPI**  
  - Quick port of a FastAPI app to Litestar  
  - Highlight differences (DI, DTOs, performance, controllers)

## Stretch Goals / Full Project Wrap-Up
- [ ] **Video #19–20+: Build a Mini Full-Stack Project**  
  - Tie everything together: auth + CRUD + WebSockets + HTMX + caching  
  - Or something fun: real-time todo board, simple blog, etc.
