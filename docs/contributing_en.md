# Contributing Guidelines

Thank you for considering contributing to the Re:lation API Python Client. This guide explains the process for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Reporting Issues](#reporting-issues)
- [Pull Requests](#pull-requests)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/0/code_of_conduct/) Code of Conduct. By participating, you are expected to uphold this code.

## Getting Started

1. Fork the project
2. Clone the repository
   ```bash
   git clone https://github.com/solahsoyalp/relation_client.git
   cd relation_client
   ```
3. Install development dependencies
   ```bash
   pip install -e ".[dev]"
   ```

## Development Setup

1. Create and activate a Python virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix-like systems
   # or
   .\venv\Scripts\activate  # Windows
   ```

2. Install dependencies
   ```bash
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks
   ```bash
   pre-commit install
   ```

## Reporting Issues

When reporting bugs, please include:

- Python version you're using
- Detailed description of the issue
- Steps to reproduce the problem
- Expected behavior and actual behavior
- Error messages and stack traces (if applicable)

For feature requests, please include:

- Detailed description of the feature
- Use cases and specific examples
- How it relates to existing functionality

## Pull Requests

1. Create a new feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Add or update tests and ensure all tests pass
   ```bash
   pytest
   ```

4. Check code style
   ```bash
   flake8
   black .
   isort .
   ```

5. Commit your changes
   ```bash
   git commit -am "Add some feature"
   ```

6. Push your changes
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a pull request: https://github.com/solahsoyalp/relation_client/pulls

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) code formatter
- Sort imports with [isort](https://pycqa.github.io/isort/)
- Add appropriate docstrings
- Use meaningful variable names and comments

## Testing

- Add tests for new features
- Ensure existing tests aren't broken
- Maintain test coverage

Running tests:
```bash
# Run all tests
pytest

# Generate coverage report
pytest --cov=relation_client tests/
```

## Documentation

- Add appropriate documentation for new features
- Update README if necessary
- Maintain code docstrings

---

*Read this in other languages: [English](contributing_en.md), [日本語](contributing.md)* 