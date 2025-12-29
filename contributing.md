# Contributing to Dataset Analysis
Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Codeof Conduct
We are committed to providing a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs
Before creating a bug report, please check the existing issues list.

To report a bug, please include:
- A clear, descriptive title
- A detailed description of the issue
- Steps to reproduce the problem
- Expected behavior
- Actual behavior
- Your environment (Python version, OS, package versions)
- Code examples or error messages

### Suggesting Enhancements
Enhancement suggestions are tracked as GitHub Issues.

To suggest an enhancement:
- Use a clear, descriptive title
- Provide a detailed description of the suggested enhancement
- List some examples of how this enhancement would be used
- Explain why this would be useful to most users


 Getting Started
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/dataset.git
   cd dataset
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8
   ```

5. Create a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```

 Development Guidelines

- Code Style: Follow PEP 8 guidelines
- Documentation: Write docstrings for all functions and classes
- Testing: Write tests for new features
- Commits: Use clear, descriptive commit messages

 Code Format

We use `black` for code formatting:
```bash
black dataset.py
```

 Linting

Check code quality with `flake8`:
```bash
flake8 dataset.py
```

 Testing

Write tests for your code:
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=./ --cov-report=html
```

### Pull Request Process

1. Update documentation if you've changed functionality
2. Add tests for new features
3. Ensure code passes linting:
   ```bash
   black --check dataset.py
   flake8 dataset.py
   ```

4. Run tests:
   ```bash
   pytest
   ```

5. Update CHANGELOG if applicable

6. Push to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```

7. Create a Pull Request with:
   - Clear title and description
   - Reference to related issues
   - List of changes made
   - Any breaking changes

8. Respond to review comments promptly

## Code Style Guidelines

### Naming Conventions

- Use `snake_case` for function and variable names
- Use `PascalCase` for class names
- Use `UPPER_CASE` for constants

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Longer description if needed, explaining the function's purpose,
    behavior, and any important details.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
    
    Returns:
        bool: Description of return value
    
    Raises:
        ValueError: When param1 is empty
    
    Examples:
        >>> function_name('test', 42)
        True
    """
    pass
```

### Comments

- Use comments to explain WHY, not WHAT
- Keep comments brief and clear
- Update comments when code changes

## Branch Naming Convention

- `feature/short-description` - New features
- `bugfix/short-description` - Bug fixes
- `docs/short-description` - Documentation changes
- `refactor/short-description` - Code refactoring

## Commit Message Guidelines

```
<type>: <subject>

<body>

<footer>
```

Type can be:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

Example:
```
feat: add outlier detection using Z-score method

Implemented Z-score based outlier detection as an alternative to IQR method.
Added parameter to choose between IQR and Z-score methods.

Closes #42
```

## Documentation

- Update README.md if you change functionality
- Add docstrings to all functions
- Include usage examples in docstrings
- Keep documentation up-to-date

## Testing

- Write unit tests for new features
- Aim for >80% code coverage
- Test edge cases
- Test error conditions

Example test:
```python
import pytest
from dataset import DatasetAnalyzer

def test_load_csv():
    analyzer = DatasetAnalyzer('test_data.csv')
    assert analyzer.df is not None
    assert analyzer.df.shape[0] > 0

def test_missing_values_with_invalid_strategy():
    analyzer = DatasetAnalyzer('test_data.csv')
    with pytest.raises(ValueError):
        analyzer.handle_missing_values(strategy='invalid')
```

## Review Process

1. At least one maintainer review required
2. All tests must pass
3. No merge conflicts
4. Code meets style guidelines
5. Documentation is complete

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md
- GitHub contributors page
- Release notes

## Questions?

- Open an issue for discussion
- Check existing issues for similar questions
- Email: your-email@example.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Dataset Analysis! 🎉
