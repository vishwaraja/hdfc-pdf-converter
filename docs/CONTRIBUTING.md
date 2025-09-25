# Contributing to HDFC PDF to CSV Converter

Thank you for your interest in contributing to the HDFC PDF to CSV Converter! This document provides guidelines and information for contributors.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. **Check existing issues** - Make sure the issue hasn't been reported already
2. **Create a new issue** - Use the appropriate issue template
3. **Provide details** - Include:
   - Python version
   - Operating system
   - PDF file details (if applicable)
   - Error messages
   - Steps to reproduce

### Submitting Code

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run tests** to ensure everything works
6. **Commit your changes** with clear commit messages
7. **Push to your fork**
8. **Create a Pull Request**

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Setup Instructions

```bash
# Clone your fork
git clone https://github.com/your-username/hdfc-pdf-converter.git
cd hdfc-pdf-converter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_converter.py
```

### Code Style

We use the following tools for code quality:

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking (if implemented)
mypy src/
```

## Coding Standards

### Python Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add support for ICICI Bank PDFs
fix: handle empty transaction rows correctly
docs: update installation instructions
test: add unit tests for categorization
```

### Code Structure

- Keep the main converter logic in `src/hdfc_converter.py`
- Add new features as separate methods
- Maintain backward compatibility
- Update documentation for new features

## Testing Guidelines

### Unit Tests

- Write tests for all new functionality
- Test edge cases and error conditions
- Mock external dependencies
- Aim for high test coverage

### Integration Tests

- Test with real PDF files (anonymized)
- Test the complete conversion workflow
- Verify output file formats

### Test Data

- Use anonymized PDF files for testing
- Create sample data for unit tests
- Don't commit sensitive financial data

## Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Include parameter descriptions and return values
- Add examples for complex functions

### User Documentation

- Update README.md for new features
- Add usage examples
- Update installation instructions if needed

### API Documentation

- Document any new public methods
- Include parameter types and return values
- Add usage examples

## Pull Request Process

### Before Submitting

1. **Run tests** - Ensure all tests pass
2. **Check code style** - Run black and flake8
3. **Update documentation** - Add docs for new features
4. **Test manually** - Verify the feature works as expected

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

1. **Automated checks** - CI/CD pipeline runs tests
2. **Code review** - Maintainers review the code
3. **Testing** - Manual testing if needed
4. **Approval** - Maintainer approves the PR
5. **Merge** - PR is merged to main branch

## Areas for Contribution

### High Priority

- **Bug fixes** - Fix reported issues
- **Performance improvements** - Optimize for large PDFs
- **Error handling** - Improve error messages and recovery
- **Documentation** - Improve user guides and examples

### Medium Priority

- **New features** - Add support for other banks
- **UI improvements** - Better CLI interface
- **Testing** - Increase test coverage
- **Code quality** - Refactor and improve code

### Low Priority

- **Nice-to-have features** - GUI interface, cloud processing
- **Advanced features** - Custom categorization, advanced filtering
- **Integration** - API endpoints, web interface

## Community Guidelines

### Be Respectful

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the code of conduct

### Communication

- Use clear, concise language
- Ask questions if something is unclear
- Provide context for issues and suggestions
- Be patient with responses

## Getting Help

### Resources

- **Documentation** - Check README and docs/
- **Issues** - Search existing issues
- **Discussions** - Use GitHub Discussions for questions
- **Email** - Contact maintainers for sensitive issues

### Questions

- **Installation issues** - Check INSTALLATION.md
- **Usage questions** - Check USAGE.md
- **Development questions** - Check this CONTRIBUTING.md
- **Bug reports** - Create an issue

## Recognition

Contributors will be recognized in:

- **README.md** - Contributor list
- **CHANGELOG.md** - Release notes
- **GitHub** - Contributor statistics
- **Releases** - Release notes

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Contact

- **Maintainer**: Vishwaraja Pathi
- **Email**: vishwaraja.pathi@adiyogitech.com
- **GitHub**: @vishwaraja

Thank you for contributing to the HDFC PDF to CSV Converter! 🎉
