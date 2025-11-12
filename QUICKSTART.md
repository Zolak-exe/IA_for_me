# 🚀 Quick Start - Multi-Agent System

Get your autonomous code generation system running in 5 minutes.

## Prerequisites

- **Python 3.10+**
- **Ollama** installed and running

## Installation

### 1. Install Ollama

**Windows:**
```powershell
winget install Ollama.Ollama
```

**Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Download a Model

```bash
# Start with a lightweight model
ollama pull mistral:latest

# Or for better code generation
ollama pull codellama:latest
```

### 3. Install Dependencies

```bash
cd multi-agent-system
pip install -r requirements.txt
```

## Usage

### Basic Example

```bash
python scripts/main.py --requirements "Create a REST API with FastAPI for task management"
```

### With Options

```bash
python scripts/main.py \
  --requirements "Build a CLI tool for file organization" \
  --max-iterations 10 \
  --threshold 85 \
  --output ./my-project \
  --verbose
```

## What Happens?

The system orchestrates 6 specialized agents:

1. **Architect** - Designs the architecture
2. **Developer** - Generates the code
3. **Reviewer** - Audits code quality
4. **Security** - Checks for vulnerabilities
5. **Tester** - Creates unit tests
6. **Documentation** - Writes docs

The system iterates until quality threshold is reached (default: 90%).

## Output

Results are saved in `./outputs/ProjectName_YYYYMMDD_HHMMSS/`:

```
project_20241112_172750/
├── SUMMARY.json          # Execution summary
├── METRICS.json          # Iteration metrics
├── ARCHITECTURE.md       # System design
├── CODE.md              # Generated code
├── TESTS.md             # Unit tests
├── DOCUMENTATION.md     # Complete docs
└── REPORT.html          # Visual report
```

## Configuration

Edit `multi-agent-system/src/config/settings.py` to customize:

- **Models**: Which LLM to use per agent
- **Thresholds**: Quality and security minimums
- **Weights**: How to score overall quality

## Common Issues

### Ollama not responding?

```bash
# Start Ollama service
ollama serve
```

### No models available?

```bash
# Download at least one model
ollama pull mistral:latest
ollama list  # Verify
```

### Out of memory?

Use smaller models in `settings.py`:

```python
AGENT_MODELS = {
    "architect": "mistral:7b",
    "developer": "mistral:7b",
    # ...
}
```

## Examples

### Web Application

```bash
python scripts/main.py --requirements "Full-stack todo app with React frontend and FastAPI backend"
```

### API Service

```bash
python scripts/main.py --requirements "RESTful API for user authentication with JWT tokens"
```

### CLI Tool

```bash
python scripts/main.py --requirements "Command-line tool to organize files by type and date"
```

### Library

```bash
python scripts/main.py --requirements "Python library for data validation with custom rules"
```

## Next Steps

- Read the [full documentation](multi-agent-system/docs/README.md)
- Customize agent models in `settings.py`
- Adjust quality thresholds for your needs
- Explore generated outputs and iterate

## Tips

- Start with simple projects to test the system
- Use `--verbose` to see detailed progress
- Lower `--threshold` for faster results (but lower quality)
- Increase `--max-iterations` for complex projects
- Check `system.log` for debugging

---

**Ready to generate code?** Run your first command and watch the agents work!
