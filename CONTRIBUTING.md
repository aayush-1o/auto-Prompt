# Contributing to AutoPrompt

Thank you for your interest in contributing to AutoPrompt! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

Feature requests are welcome! Please include:
- Use case description
- Proposed solution
- Any alternatives considered

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow PEP 8 style guidelines
   - Add tests for new functionality

4. **Run tests**
   ```bash
   pytest
   ```

5. **Commit with descriptive messages**
   ```bash
   git commit -m "feat: add new scoring metric"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/auto-Prompt.git
cd auto-Prompt

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest --cov=src
```

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and testable

## Testing

- Write tests for new features
- Maintain test coverage above 60%
- Use pytest fixtures for repeated setup

## Questions?

Feel free to open an issue for any questions!

---

Thank you for contributing! 🚀
