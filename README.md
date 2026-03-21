# Testomat E2E Testing Framework

A Playwright-based End-to-End (E2E) testing framework designed for testing the Testomat application.

## Overview

This project uses Python, Playwright, and Pytest to perform automated UI testing. It follows the Page Object Model (POM) and component-based architecture to make tests readable, maintainable, and scalable.

## Technologies Used
- **Python** (>= 3.14)
- **Playwright** (`playwright`, `pytest-playwright`) for browser automation
- **Pytest** for the testing framework
- **pytest-html** for generating HTML test reports
- **Faker** for generating test data
- **python-dotenv** for environment variable management
- **uv** for dependency management
- **Ruff** for linting and code formatting

## Project Structure

```text
testomat_tests/
├── src/                # Source code (Page Objects, Components, App config)
│   ├── web/            # Web application models
│   │   ├── pages/      # Page Object Models (POM)
│   │   ├── components/ # Reusable UI components
│   │   └── app.py      # Main application interface/facade
│   └── config.py       # Configuration and Environment variables loading
├── tests/              # Test files
│   ├── web/            # UI Tests
│   └── conftest.py     # Pytest configuration and fixtures
├── test-result/        # Generated reports and Playwright traces
├── pytest.ini          # Pytest settings and markers configuration
├── pyproject.toml      # Project dependencies and metadata
├── ruff.toml           # Ruff linter configuration
└── .env                # Environment variables (needs to be created)
```

## Setup and Installation

1. **Clone the repository**

2. **Setup Environment Variables**
   Create a `.env` file in the root directory based on the configuration expected in `src/config.py`.
   ```env
   BASE_URL=https://app.testomat.io
   BASE_APP_URL=https://app.testomat.io/users/sign_in
   EMAIL=your_test_email@example.com
   PASSWORD=your_test_password
   ```

3. **Install Dependencies**
   This project uses `uv` for dependency management.
   ```bash
   uv sync
   ```

4. **Install Playwright Browsers**
   ```bash
   uv run playwright install --with-deps
   ```

## Running the Tests

Tests are executed using `pytest`. Default settings (like running headed mode and generating HTML reports) are already configured in `pytest.ini`.

To run all tests:
```bash
uv run pytest
```

To run a specific test file:
```bash
uv run pytest tests/web/login_page_tests.py
```

To run tests with a specific marker (e.g., `smoke`):
```bash
uv run pytest -m smoke
```

To run tests in headless mode (overriding the default headed behavior in `pytest.ini`):
```bash
uv run pytest --headed=False
```

## Test Reports and Traces
- **HTML Report:** Generated automatically at `test-result/report.html` after a test run.
- **Playwright Traces:** Saved in `test-result/traces/`. You can view them using the Playwright Trace Viewer:
  ```bash
  uv run playwright show-trace test-result/traces/<trace-file>.zip
  ```

## Development and Linting
The project uses `ruff` for code linting and formatting.
```bash
uv run ruff check .
```
