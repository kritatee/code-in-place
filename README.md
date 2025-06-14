# ArXiv Paper Downloader with Citations

A Python tool that searches for academic papers on arXiv, downloads them with their citations, and organizes them in a structured folder hierarchy.

## Features

- Search arXiv papers by keyword
- Download papers as PDF files
- Create timestamped folders for organization
- Extract and download arXiv citations automatically
- Organized folder structure with citations subfolder

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the program:

```bash
python main.py
```

The program will prompt you to enter search terms. For each paper found:

1. Creates a folder: `<timestamp>-<paper_name>/`
2. Downloads the main paper PDF
3. Creates a `citations/` subfolder
4. Extracts arXiv citations from the abstract/title
5. Downloads citation PDFs to the citations folder

## Folder Structure

```
20231214_143022-Attention_Is_All_You_Need/
├── 1706.03762.pdf              # Main paper
└── citations/
    ├── 1409.0473_Neural_Machine.pdf
    └── 1508.04025_Effective_Approach.pdf
```

## Dependencies

- `arxiv` - For accessing arXiv API
- `requests` - For downloading PDF files
- `pathlib` - For file system operations (built-in)
- `re` - For citation extraction (built-in)

## Limitations

- Currently only extracts arXiv citations from abstracts/titles
- Does not parse full PDF content for citations
- Limited to papers available on arXiv

Type 'exit' to quit the program.