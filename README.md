# Factory Compliance & Industrial Safety System

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](dockerfile)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Docker Deployment](#docker-deployment)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🎯 Overview

Factory Compliance & Industrial Safety System is an enterprise-grade, AI-powered platform designed to monitor and enforce factory safety policies in real-time. The system combines edge-based computer vision (YOLOv8) with cloud-based AI verification (OpenRouter VLM) to detect policy violations, escalate incidents, and generate comprehensive compliance reports.

<img width="2752" height="1536" alt="Gemini_Generated_Image_dl3fzjdl3fzjdl3f" src="https://github.com/user-attachments/assets/e6dea2f1-6124-4ad3-804f-69ca11adb321" />



### Key Capabilities

- **Real-time Safety Monitoring**: Continuous surveillance of factory floor operations using advanced computer vision
- **Policy Enforcement**: Automatic parsing and enforcement of complex safety policies from PDF documents
- **Intelligent Escalation**: Context-aware incident escalation with severity assessment
- **Compliance Reporting**: Automated generation of compliance reports in multiple formats (CSV, JSON, PDF)
- **Industrial Dashboard**: Real-time supervision interface with enterprise-grade UI/UX

<img width="2816" height="1536" alt="Gemini_Generated_Image_1ftp0p1ftp0p1ftp" src="https://github.com/user-attachments/assets/8442f5e6-dc62-42b1-b77b-aa3cc828d23e" />


## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|------------|
| **Hybrid Detection** | Edge-based YOLOv8 + Cloud-based VLM for accuracy and speed |
| **Policy Parsing** | AI-powered extraction of compliance rules from PDF policies |
| **Zone Management** | Geometric region-of-interest (ROI) detection and tracking |
| **Severity Classification** | Automated risk assessment with configurable severity matrices |
| **Real-time Alerts** | Immediate escalation of detected violations with audit trails |
| **Report Generation** | Multi-format compliance reports (CSV, JSON, PDF) with detailed analytics |
| **Dashboard UI** | Streamlit-based industrial control panel with live metrics |
| **Database Persistence** | SQLite backend for violation history and compliance tracking |

### Technical Highlights

- **Edge Computing**: Local YOLOv8 inference for low-latency detection
- **Cloud Verification**: OpenRouter VLM for complex safety context analysis
- **Containerization**: Docker support for consistent deployment across environments
- **Scalable Architecture**: Modular design supporting multi-zone, multi-camera deployments
- **API Integration**: OpenAI/OpenRouter for advanced NLP and vision capabilities

<img width="2752" height="1536" alt="Gemini_Generated_Image_nhlsqfnhlsqfnhls" src="https://github.com/user-attachments/assets/5689fcff-f467-42ba-9562-3362002d86d8" />


## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FACTORY FLOOR INPUT                       │
│                 (Video Feeds / Image Streams)                │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │  EDGE PROCESSOR    │
        │  (YOLOv8 Local)    │
        │  - Spatial Tracking│
        │  - ROI Detection   │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────────┐
        │ CLOUD VERIFICATION     │
        │ (OpenRouter VLM)       │
        │ - Context Analysis     │
        │ - Complex Validation   │
        └─────────┬──────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ SEVERITY │ │ESCALATION│ │ REPORT   │
│ MATRIX   │ │ ENGINE   │ │GENERATOR │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │
     └────────────┼────────────┘
                  │
        ┌─────────▼──────────┐
        │  DATABASE (SQLite) │
        │  - Violations Log  │
        │  - Alert History   │
        │  - Audit Trail     │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │    DASHBOARD UI    │
        │  (Streamlit App)   │
        │  - Live Metrics    │
        │  - Report Viewer   │
        │  - Alert Console   │
        └────────────────────┘
```
<img width="2816" height="1536" alt="Gemini_Generated_Image_qof2p4qof2p4qof2" src="https://github.com/user-attachments/assets/17f9adbb-9f7d-4d72-bbb4-d192a2f45314" />

### Module Breakdown

| Module | Purpose |
|--------|---------|
| `policy_parser.py` | Extracts compliance rules from PDF using OpenAI |
| `detector.py` | Hybrid detection engine (YOLOv8 + VLM verification) |
| `escalation_engine.py` | Alert management and incident escalation |
| `severity_matrix.py` | Risk classification and severity scoring |
| `report_generator.py` | Multi-format report generation (CSV, JSON, PDF) |
| `app.py` | Streamlit dashboard and UI interface |

## 📋 Prerequisites

### System Requirements

- **OS**: Linux, macOS, or Windows (with WSL2 recommended)
- **Python**: 3.11 or higher
- **RAM**: 8GB minimum (16GB+ recommended for high-throughput)
- **GPU** (Optional): CUDA 11.8+ for accelerated inference (recommended)
- **Storage**: 10GB+ for model weights and database

### API Credentials

You'll need API keys for:

1. **OpenRouter API**: For LLM and VLM capabilities
   - Sign up at [OpenRouter](https://openrouter.ai)
   - Minimum recommended balance: $5-10 for testing

2. **Optional**: Direct OpenAI API key (if not using OpenRouter)

### Pre-downloaded Models

- **YOLOv8 Nano**: `yolov8n.pt` (included in repo)
  - If missing, automatically downloaded on first use
  - Alternative: `yolov8s.pt` or `yolov8m.pt` for higher accuracy

## 🚀 Installation

### Option 1: Local Installation (Recommended for Development)

```bash
# 1. Clone the repository
git clone <repository-url>
cd Factory_ComplianceProject

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create environment file
cp .env.example .env
# Edit .env with your API keys
```

### Option 2: Docker Installation (Recommended for Production)

```bash
# Build the Docker image
docker build -t factory-compliance:latest .

# Run the container
docker run -p 8501:8501 \
  -e OPENROUTER_API_KEY=<your-key> \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/data:/app/data \
  factory-compliance:latest
```

### Option 3: Docker Compose (Recommended for Full Stack)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Configuration
OPENROUTER_API_KEY=<your-openrouter-api-key>
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Model Configuration
YOLO_MODEL=yolov8n.pt
VLM_MODEL=mistralai/mistral-7b-instruct:free  # or any available OpenRouter model

# Feature Flags
ENABLE_VLM_VERIFICATION=true
ENABLE_PDF_PARSING=true
ENABLE_REPORT_EXPORT=true

# Logging
LOG_LEVEL=INFO
DEBUG_MODE=false

# Database
DATABASE_PATH=outputs/compliance.db

# Thresholds
CONFIDENCE_THRESHOLD=0.5
ESCALATION_THRESHOLD=0.7
```

### Detection Configuration

Configure detection parameters in detector initialization:

```python
from src.detection.detector import EdgeProcessor

# Create processor with custom configuration
processor = EdgeProcessor(
    model_path="yolov8n.pt",
    confidence_threshold=0.5,
    iou_threshold=0.45
)
```

### Policy Configuration

Place your safety policy PDFs in the project root or specify a custom path:

```python
from src.policy_parser import extract_text_from_pdf, parse_rules_with_openrouter

pdf_path = "path/to/your/safety_policy.pdf"
policy_text = extract_text_from_pdf(pdf_path)
rules = parse_rules_with_openrouter(policy_text)
```

## 📖 Usage

### Running the Dashboard

```bash
# Start the Streamlit dashboard
streamlit run src/dashboard/app.py

# Dashboard will be available at: http://localhost:8501
```

### Batch Processing

```bash
# Process a batch of images from evaluation directory
python -c "
from src.detection.detector import EdgeProcessor
from src.reports.report_generator import ReportGenerator

processor = EdgeProcessor()
generator = ReportGenerator()

# Process batch
violations = processor.process_batch('data/evaluation_batch/')

# Generate report
generator.generate_report(violations, output_format='json')
"
```

### Policy Parsing

```bash
# Extract and parse safety policies from PDF
python -c "
from src.policy_parser import extract_text_from_pdf, parse_rules_with_openrouter

policy_text = extract_text_from_pdf('policy.pdf')
rules = parse_rules_with_openrouter(policy_text)

import json
with open('outputs/extracted_rules.json', 'w') as f:
    json.dump(rules, f, indent=2)
"
```

### Violation Detection

```bash
# Detect violations in video/images
python -c "
from src.detection.detector import EdgeProcessor
from src.severity.severity_matrix import SeverityMatrix
from src.escalation.escalation_engine import EscalationEngine

processor = EdgeProcessor()
severity_engine = SeverityMatrix()
escalation = EscalationEngine()

# Process detection
detections = processor.process_image('path/to/image.jpg')

# Assess severity
for detection in detections:
    severity = severity_engine.calculate_severity(detection)
    escalation.log_violation(detection, severity)
"
```

## 📁 Project Structure

```
Factory_ComplianceProject/
├── src/
│   ├── policy_parser.py           # PDF policy extraction & parsing
│   ├── detection/
│   │   └── detector.py            # YOLOv8 + VLM hybrid engine
│   ├── escalation/
│   │   └── escalation_engine.py   # Alert management
│   ├── severity/
│   │   └── severity_matrix.py     # Risk classification
│   ├── reports/
│   │   └── report_generator.py    # Multi-format reporting
│   └── dashboard/
│       └── app.py                 # Streamlit UI
├── data/
│   └── evaluation_batch/          # Sample test images/videos
├── outputs/
│   ├── compliance_report.csv      # Generated reports
│   ├── compliance_report.json     # JSON format
│   ├── extracted_rules.json       # Parsed policies
│   ├── raw_detections.json        # Detection data
│   ├── violations_with_severity.json
│   ├── crops/                     # Cropped violation images
│   └── compliance.db              # SQLite database
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── dockerfile                     # Docker image definition
├── docker-compose.yml             # Multi-container setup
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── yolov8n.pt                    # Pre-trained YOLO model
├── test_key.py                    # API testing utility
└── README.md                      # This file
```

## 🔌 API Reference

### EdgeProcessor

**Module**: `src.detection.detector`

```python
from src.detection.detector import EdgeProcessor

processor = EdgeProcessor()

# Process single image
detections = processor.process_image(image_path)
# Returns: List of detection objects with coordinates, class, confidence

# Process batch
batch_results = processor.process_batch(directory_path)
# Returns: Aggregated detection results with timestamps
```

### ReportGenerator

**Module**: `src.reports.report_generator`

```python
from src.reports.report_generator import ReportGenerator

generator = ReportGenerator()

# Generate CSV report
generator.generate_report(violations, format='csv', output_path='outputs/report.csv')

# Generate JSON report
generator.generate_report(violations, format='json', output_path='outputs/report.json')

# Generate PDF report
generator.generate_report(violations, format='pdf', output_path='outputs/report.pdf')
```

### EscalationEngine

**Module**: `src.escalation.escalation_engine`

```python
from src.escalation.escalation_engine import EscalationEngine, get_active_alerts

engine = EscalationEngine()

# Log violation
engine.log_violation(detection, severity_level='HIGH')

# Get active alerts
active_alerts = get_active_alerts()
# Returns: List of unresolved incidents

# Generate compliance CSV
engine.generate_compliance_csv(output_path='outputs/compliance.csv')
```

### SeverityMatrix

**Module**: `src.severity.severity_matrix`

```python
from src.severity.severity_matrix import SeverityMatrix

severity = SeverityMatrix()

# Calculate severity score
score = severity.calculate_severity(detection_obj)
# Returns: Severity level (LOW, MEDIUM, HIGH, CRITICAL)
```

## 🐳 Docker Deployment

### Building the Image

```bash
docker build -t factory-compliance:latest .
```

### Running Single Container

```bash
docker run -p 8501:8501 \
  -e OPENROUTER_API_KEY=sk_xxxx \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/data:/app/data \
  factory-compliance:latest
```

### Using Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    volumes:
      - ./outputs:/app/outputs
      - ./data:/app/data
    restart: unless-stopped
```

```

## 🔧 Troubleshooting

### Common Issues

#### 1. **ModuleNotFoundError: No module named 'openai'**

```bash
# Ensure dependencies are installed
pip install --upgrade -r requirements.txt

# Verify installation
python -c "import openai; print(openai.__version__)"
```

#### 2. **API Key Errors**

```bash
# Verify .env file exists and contains correct keys
cat .env | grep OPENROUTER_API_KEY

# Test API connectivity
python test_key.py
```

#### 3. **Streamlit Port Already in Use**

```bash
# Run on custom port
streamlit run src/dashboard/app.py --server.port 8502
```

### Getting Help

1. Check logs: `tail -f logs/compliance.log`
2. Enable debug mode in `.env`: `DEBUG_MODE=true`
3. Test API connectivity: `python test_key.py`
4. Review OpenRouter dashboard for quota/billing issues

## 👥 Contributing

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt pytest black flake8

# Run tests
pytest tests/

# Format code
black src/

# Lint code
flake8 src/
```

### Pull Request Process

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test thoroughly
3. Commit with clear messages: `git commit -m "Add feature: ..."`
4. Push to branch: `git push origin feature/your-feature`
5. Submit pull request with description

### Code Standards

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints where applicable
- Write unit tests for new features
- Update README for new capabilities

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
