# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
- Development server: `uv run uvicorn --reload web.server:app`
- With Docker: `docker compose -f docker-compose.dev.yaml up`
- App runs at `http://localhost:8000`

### Code Quality & Testing
- Install dependencies: `uv sync`
- Run tests: `uv run pytest`
- Type checking: `uv run mypy .`
- Linting: `uv run ruff check`
- Auto-fix linting: `uv run ruff check --fix`
- Format code: `uv run ruff format`

## Project Architecture

This is the homepage for The Ludic Framework (https://github.com/getludic/ludic), built entirely using Ludic itself. The project demonstrates Ludic's capabilities through interactive demos, comprehensive documentation, and a component catalog.

### Core Structure
- **web/server.py**: Main FastAPI application with Ludic integration, includes lifespan management for search indexing
- **web/pages.py**: Base page components including `BasePage`, `Page`, and `HomePage` with shared styling and layouts
- **web/config.py**: Environment-based configuration with sensible defaults
- **web/themes.py**: Custom theme implementation for consistent styling across the site

### Key Modules

#### Endpoints Organization
- **web/endpoints/index.py**: Homepage with interactive code samples and rotating demos
- **web/endpoints/catalog/**: Component catalog showcasing typography, buttons, forms, layouts, messages, tables, and loaders
- **web/endpoints/docs/**: Comprehensive documentation including getting started guides, component guides, HTMX integration, and styling
- **web/endpoints/demos/**: Interactive HTMX demos (bulk update, click-to-edit, lazy loading, infinite scroll, etc.)
- **web/endpoints/examples/**: Code examples corresponding to the demos
- **web/endpoints/search.py**: Full-text search functionality with TF-IDF ranking
- **web/endpoints/status.py**: Health check and status endpoint

#### Search System
- **web/search/index.py**: Custom search index implementation with TF-IDF scoring
- **web/search/documents.py**: Document structure for search indexing
- **web/search/analysis.py**: Text analysis and tokenization for search
- Search index is built at startup using `build_index()` from all documentation and catalog pages

#### Components & Styling
- **web/components.py**: Reusable components like headers, footers, menus, and edit-on-GitHub links
- **web/middlewares.py**: Cookie storage middleware and optional profiling middleware
- **web/database.py**: In-memory database for demo functionality using cookies for persistence

### Testing Strategy
- Uses pytest with Starlette's TestClient
- Tests focus on endpoint functionality and demo interactions
- Cookie-based state management is tested through database serialization
- All demo endpoints have corresponding tests ensuring HTMX interactions work correctly

### Development Patterns
- Component-based architecture using Ludic's type-safe components
- Extensive use of HTMX for dynamic interactions without JavaScript
- Theme-aware styling using Ludic's built-in theming system
- Mount-based routing for organizing related endpoints
- Environment variable configuration with defaults for development

### Key Dependencies
- **ludic[full]**: The core framework providing components
- **uvicorn**: ASGI server for development and production
- **pystemmer**: Text stemming for search functionality
- **httpx**: HTTP client for testing
- **pytest**: Testing framework

### Special Features
- View transitions for smooth UX (see CodeSample component in index.py)
- Full-text search with custom indexing and ranking
- Interactive code samples that cycle through different Ludic patterns
- Responsive design with careful attention to mobile experience
- SEO optimization with proper meta tags and Open Graph support
