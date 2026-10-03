# LangChain Multi-Agent Research System

A small AI research assistant that searches the web for a topic, extracts useful content from a source, drafts a structured report, and asks an AI critic to review it. The project includes a Streamlit interface for running the workflow and viewing or downloading its results.

## Features

- Search the web for relevant research using Tavily.
- Extract readable text from a selected web page.
- Generate a structured report with findings, a conclusion, and sources.
- Review the report with a separate critic prompt.
- View search results, extracted content, the report, and critic feedback in a Streamlit app.
- Download the generated report as Markdown.

## Technology

| Area | Technology |
| --- | --- |
| Language | Python 3.11+ |
| User interface | Streamlit |
| Agent and chain orchestration | LangChain |
| Language model | OpenAI-compatible ChatOpenAI client via OpenRouter |
| Web search | Tavily |
| Page extraction | Requests and BeautifulSoup |
| Configuration | python-dotenv |

## Requirements

- Python 3.11 or newer
- An [OpenRouter API key](https://openrouter.ai/)
- A [Tavily API key](https://tavily.com/)

## Installation

Clone the repository and enter its directory:

```bash
git clone https://github.com/ggswineroom/LangChain-Multi-Agent-Research-System.git
cd LangChain-Multi-Agent-Research-System
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root and add your API keys:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Keep this file private. `.env` is ignored by Git; do not commit API keys or other credentials.

## Run the application

Start the Streamlit interface from the project root:

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit, enter a research topic, and choose **Start Research**. The app displays the search results, extracted page content, generated report, and critic feedback. Use **Download Report** to save the report as Markdown.

The `main.py` script also demonstrates running the pipeline directly; it currently uses a sample topic defined in the script.

## Architecture

The application is organized as a sequential research pipeline:

```text
Streamlit UI (app.py)
        |
        v
Research pipeline (src/pipelines/pipeline.py)
        |
        +--> Search agent --> Tavily web search
        |
        +--> Reader agent --> URL selection and page extraction
        |
        +--> Writer chain --> structured research report
        |
        +--> Critic chain --> score, strengths, and improvement notes
        |
        v
Results returned to the UI for display and download
```

- `src/agents/agents.py` configures the model, search and reader agents, and writer and critic chains.
- `src/tools/tools.py` provides the Tavily search and web-page extraction tools.
- `src/pipelines/pipeline.py` runs each stage and collects its outputs.
- `app.py` provides the interactive Streamlit interface.

The model calls use `ChatOpenAI` configured with OpenRouter's API endpoint. Web search and page extraction require network access, and some websites may restrict automated access.

## Contributing

Contributions are welcome. Open an issue to discuss a bug or proposed change, or submit a pull request with a focused change and a clear description.

## License

This project is licensed under the Apache License 2.0. See [LICENSE](./LICENSE) for the full license text.
