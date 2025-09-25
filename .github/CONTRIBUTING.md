# Contributing to HDFC PDF Converter

Thank you for your interest in contributing to the HDFC PDF Converter project! This document provides guidelines and information for contributors.

## Development Workflow

### Branch Protection Rules
- **Main branch protection**: All changes to the `main` branch must go through a pull request
- **Required approvals**: At least 1 approval from code owners is required
- **Status checks**: All CI tests must pass before merging
- **Auto-deployment**: Changes merged to `main` automatically deploy to Railway

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/hdfc-pdf-converter.git
   cd hdfc-pdf-converter
   ```

3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes** and test them locally

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## CI/CD Pipeline

### What happens on Pull Requests:
1. **Code Tests**: Python tests run on multiple versions (3.9, 3.10, 3.11)
2. **Docker Build**: Docker image is built and tested
3. **Health Check**: Container health endpoint is verified
4. **Approval Required**: Code owner approval is required before merge

### What happens on Main Branch Push:
1. **All PR checks** run again
2. **Automatic Deployment**: Changes are deployed to Railway
3. **Health Verification**: Deployed application is tested

## Local Development

### Prerequisites
- Python 3.9+
- Docker
- Git

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Build Docker image
docker build -t hdfc-converter .

# Run locally
docker run -p 5000:5000 hdfc-converter
```

### Testing
- Write tests for new features
- Ensure all existing tests pass
- Test with different PDF sizes and formats

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Include type hints where appropriate

## Pull Request Guidelines

### Before Submitting:
- [ ] All tests pass locally
- [ ] Code follows project style guidelines
- [ ] Documentation is updated if needed
- [ ] No sensitive information is included

### PR Title Format:
- `Add: description` for new features
- `Fix: description` for bug fixes
- `Update: description` for improvements
- `Docs: description` for documentation changes

### PR Description:
- Use the provided PR template
- Describe what changes were made
- Explain why the changes were necessary
- Include any relevant screenshots or test results

## Deployment

### Automatic Deployment
- Changes merged to `main` automatically deploy to Railway
- Deployment URL: `https://web-production-5925.up.railway.app`
- Health check endpoint: `/health`

### Manual Deployment
If you need to deploy manually:
```bash
# Using Railway CLI
railway up --service web

# Using Docker
docker run -p 5000:5000 vishwa86/hdfc-pdf-converter:latest
```

## Security

- Never commit sensitive information (API keys, passwords, etc.)
- Use GitHub Secrets for environment variables
- Report security issues privately to the maintainer

## Getting Help

- Check existing issues and discussions
- Create a new issue for bugs or feature requests
- Use the provided issue templates

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
