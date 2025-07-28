# Smart PDF Structure Extractor

This tool automatically extracts structured outlines (Title, H1, H2, H3 with page numbers) from PDF documents. It's designed to work offline and handle multilingual content effectively. This project was developed for the Adobe India Hackathon – Connecting the Dots (Round 1A).

## 🎯 Features

- **Title Detection**: Smart detection of document titles with format preservation
- **Heading Extraction**: Automatically identifies H1, H2, H3 headings based on:
  - Font size and style
  - Text positioning
  - Format characteristics
  - Content patterns
- **Page Mapping**: Accurate page numbers for each heading
- **Format Preservation**: Maintains original text formatting
- **Offline Processing**: Works completely offline
- **Multilingual Support**: Works with multiple languages (tested with Hindi/English)
- **Docker Support**: Platform-independent execution
- **Fast Processing**: Handles 50-page documents in under 10 seconds

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (for local installation)
- Docker (recommended)
- 200MB free disk space
- PDF files to process

### Option 1: Using Docker (Recommended)

1. Build the Docker image:
```bash
docker build --platform linux/amd64 -t smartpdfextractor:v1 .
```

2. Run the container:
Windows (CMD):
```bash
docker run --rm -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" --network none smartpdfextractor:v1
```

Windows (PowerShell):
```powershell
docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" --network none smartpdfextractor:v1
```

Linux/macOS:
```bash
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" --network none smartpdfextractor:v1
```

### Option 2: Local Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Download spaCy English model:
```bash
python -m spacy download en_core_web_sm
```

3. Run the extractor:
```bash
python main.py
```

## 📁 Project Structure

```
.
├── input/                  # Place PDF files here
├── output/                # JSON outputs appear here
├── main.py               # Main extraction logic
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
└── README.md            # This documentation
```

## 🔍 How It Works

1. **Title Detection**:
   - Analyzes first page content
   - Considers font size, position, and formatting
   - Uses smart scoring system for accurate title identification

2. **Heading Detection**:
   - H1: Largest font size (≥18pt) or prominent formatting
   - H2: Medium font size (≥16pt) or bold formatting
   - H3: Smaller font size (≥14pt) with distinct formatting

3. **Content Processing**:
   - Removes duplicate entries
   - Filters out non-heading text
   - Preserves hierarchical structure
   - Maps page numbers accurately

## 📄 Output Format

Each processed PDF generates a JSON file with the following structure:
```json
{
  "title": "Document Title",
  "outline": [
    {
      "text": "Heading Text",
      "level": "H1",
      "page": 1
    },
    {
      "text": "Subheading",
      "level": "H2",
      "page": 2
    },
    {
      "text": "Detailed Section",
      "level": "H3",
      "page": 3
    }
  ]
}
```

## ⚙️ Technical Specifications

### Performance
- ✅ Processing Time: Under 10 seconds for 50 pages
- ✅ Memory Usage: Efficient memory management
- ✅ CPU Usage: Optimized for standard CPUs

### Compliance
- ✅ No external API or internet dependency
- ✅ Runs on amd64 CPU architecture
- ✅ Model/Code size under 200MB
- ✅ Multilingual support
- ✅ Platform independent via Docker

## 🛠️ Troubleshooting

1. **Docker Issues**:
   - Ensure Docker is running
   - Check volume mount permissions
   - Verify platform compatibility

2. **PDF Processing Issues**:
   - Ensure PDFs are not password-protected
   - Check file permissions
   - Verify PDF isn't corrupted

3. **Output Issues**:
   - Check input/output folder permissions
   - Ensure enough disk space
   - Verify JSON file formatting

## 🔒 Security Notes
- Completely offline processing
- No external API calls
- Local file processing only
- Docker container isolation
- No data leaves your system
