# AutoPrompt MVP Benchmark

A Python-based benchmark system for evaluating AutoPrompt performance using Google's Gemini AI models for review processing and data extraction.

## Features

- **Baseline Pipeline**: Standard review processing
- **AutoPrompt Engine**: Advanced prompt engineering for improved extraction
- **Evaluation System**: Compare baseline vs AutoPrompt performance
- **Rate Limiting**: Built-in support for API free tier limits

## Prerequisites

- Python 3.8+
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd autoprompt
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**
   
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_key_here
   ```

## Usage

Run the benchmark:
```bash
python main.py
```

The script will:
- Process 20 reviews (configurable in `main.py`)
- Run baseline pipeline
- Run AutoPrompt pipeline
- Generate comparison report in `results/benchmark_report.json`

**Note**: The script includes rate limiting for free tier API usage (10 req/min).

## Project Structure

```
autoprompt/
├── config/          # Configuration files
├── data/            # Review data and ground truth
├── logs/            # Runtime logs
├── results/         # Benchmark results
├── src/             # Source code
│   ├── autoprompt.py    # AutoPrompt engine
│   ├── baseline.py      # Baseline pipeline
│   ├── evaluator.py     # Evaluation logic
│   └── utils.py         # Utility functions
├── main.py          # Entry point
└── requirements.txt # Dependencies
```

## License

MIT
