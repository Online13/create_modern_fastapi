# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

This is a **CLI tool** (`create-modern-fastapi`) that scaffolds new FastAPI projects using Clean Architecture. It is published as a package and invoked via `uvx create-modern-fastapi`. The `template/` directory contains the actual project scaffold that gets copied to the user's target directory.

There are therefore **two distinct codebases** here:
1. `src/create_modern_fastapi/` — the CLI tool itself
2. `template/` — the FastAPI project template that gets generated

## Commands (CLI tool development)

```bash
uv sync                  # Install dependencies
uv run create-modern-fastapi          # Run the CLI interactively
uv run create-modern-fastapi create <path>   # Create a project non-interactively
uv run create-modern-fastapi add <entity>    # Add entity (migration|module|service|use_case)
```

## Commands (inside a generated project)

The generated project uses `justfile` + `uv`. Run these from the generated project root:

```bash
just dev                          # Run dev server with hot reload
just start                        # Run production server
just test-unit                    # Run unit tests
just test-coverage                # Run unit tests with coverage report
just test-clean                   # Run clean architecture dependency rule tests
just makemigration "<comment>"    # Generate Alembic migration
just migrate                      # Apply migrations (alembic upgrade head)
just check                        # Check for unapplied migrations
just logmigration                 # View migration history
uv run ruff check .               # Lint
uv run ruff format .              # Format
```

## CLI Architecture (`src/create_modern_fastapi/`)

- `cli.py` — Click entrypoint with `create` and `add` commands
- `service.py` — Thin orchestration layer called by the CLI
- `domain.py` — `EntityType` enum (migration, module, service, use_case)
- `commands/create.py` — Copies `template/` to target path, renders `.jinja` files with Jinja2, optionally runs `git init`
- `commands/add/registry.py` — Maps `EntityType` to handler functions
- `commands/add/add_*.py` — Individual entity-add handlers (mostly stubs)

Template files ending in `.jinja` are rendered with `project_name` and `project_description` as context variables, then the `.jinja` extension is removed.

## Generated Project Architecture (`template/`)

Follows Clean Architecture with strict layer dependency rules enforced by tests using `grimp`.

```
main.py                    # Entry: initializes Settings, DB engine, creates FastAPI app
src/
  container.py             # Class-based service locator (holds engine + settings)
  domain/
    entities/              # Domain entities
    value_objects/         # Value objects
    exceptions/            # DomainException hierarchy (core.py, auth.py)
    interfaces/
      repositories/        # Repository interfaces
      services/            # Service interfaces
  infrastructure/
    env/env.py             # pydantic-settings Settings class; setup_settings() stores in Container
    persistence/database/
      database.py          # setup_database(), get_db_session() async generator
      models/
        base_models.py     # BaseSQLModel (id PK) and TimestampedModel (created_at/updated_at)
        app_models.py      # App-specific SQLModel table models
  security/
    auth_doc/              # HTTP Basic auth guard for /docs endpoint
  modules/
    doc/                   # FastAPI /docs route with auth protection
    <feature>/             # Each feature is a module here
  presentation/
    app.py                 # create_app() wires FastAPI, error handlers, routers
    deps/
      repository.py        # DatabaseDep = Annotated[AsyncSession, Depends(get_db_session)]
      service.py           # Service dependencies
      env.py               # Settings dependency
    entities/response.py   # Generic Response[T] and PaginatedResponse[T] Pydantic models
    error/
      error_handler.py     # bind() registers exception handlers; create_error_response() for route docs
      error_schema.py      # Pydantic error response schemas
```

### Dependency Flow

```
main.py → presentation → application/use_cases → domain
                       → infrastructure → domain
```

Infrastructure and presentation layers must not import from each other directly; they meet at the domain interfaces. The `tests/clean/` suite verifies this with `grimp`.

### Key Patterns

- **Container**: Singleton class used as a service locator. Call `Container.set_*` at startup (`main.py`) and `Container.get_*` inside the app. Not a DI framework — just a global holder.
- **Error handling**: Raise `DomainException` subclasses (e.g., `NotFoundException`, `ConflictException`) anywhere in domain/application code. `error_handler.bind(app)` catches them and returns the correct HTTP status. Auth errors use `AuthDomainException` subclasses → 401.
- **Response shape**: All routes return `Response[T]` (`{success, message, data}`) or `PaginatedResponse[T]` (`{success, message, data, meta}`).
- **Database models**: Extend `BaseSQLModel` for auto `id` + timestamps, or `TimestampedModel` without `id`.
- **Linting**: ruff with tab indentation (indent-width = 3), line-length 88, quote-style double.
- **Database driver**: `psycopg` (v3, async-compatible), not `psycopg2`. Connection strings use `postgresql+psycopg://`.
