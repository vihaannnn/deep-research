# Deep Research

Deep Research is an advanced news search and analysis application inspired by Perplexity's Deep Research functionality. It empowers users to search for information across the web, automatically extract relevant content, distill key insights, and generate comprehensive research reports using AI.

## Overview

Deep Research automates the research process through a multi-stage pipeline:

1. **Query Enhancement**: Optimizes user queries for more effective searches
2. **Web Search**: Retrieves relevant URLs from search engines
3. **Content Extraction**: Scrapes and cleans content from web pages
4. **Information Distillation**: Processes articles to extract key insights
5. **Report Generation**: Creates comprehensive, well-structured reports

## Features

- **Smart Query Enhancement**: Uses GPT-3.5 to optimize search terms
- **Selective Recency**: Option to focus on recent content or include historical sources
- **Automatic Content Extraction**: Scrapes and cleans webpage content
- **Content Distillation**: Uses GPT-4 to extract the most relevant information from each source
- **Comprehensive Report Generation**: Creates detailed analysis reports across multiple sources
- **Streamlit UI**: User-friendly interface with tabs for different views and functions

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- Google Search API key (optional)

### Setting Up on Mac

1. Clone the repository:
   ```bash
   https://github.com/vihaannnn/deep-research.git
   cd deep-research
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Setting Up on Windows

1. Clone the repository:
   ```cmd
   https://github.com/vihaannnn/deep-research.git
   cd deep-research
   ```

2. Create and activate a virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Enter a search query in the text input field
3. Choose whether you want only recent news
4. Click "Search" to retrieve results
5. Explore the results in different tabs:
   - **URLs Only**: Quick overview of source URLs
   - **Detailed View**: Full content from each source
   - **Distilled Content**: AI-processed key information from each article
   - **Generate Report**: Create a comprehensive analysis based on the collected data

## Data Pipeline

The application's data pipeline consists of several stages:

1. **Query Enhancement**:
   - User input is processed by GPT-3.5 to create an optimized search query
   - Recently filters are applied if selected

2. **Web Search**:
   - The enhanced query is sent to Google Search
   - Top results are collected for further processing

3. **Content Extraction**:
   - Each URL is accessed with appropriate headers
   - HTML content is parsed using BeautifulSoup
   - Publication dates are extracted when available
   - Content is cleaned and truncated if necessary

4. **Information Distillation**:
   - OpenAI's o1 model processes each article to extract key information
   - All relevant facts, quotes, statistics, and insights are preserved
   - Results are formatted as bulleted lists for readability

5. **Report Generation**:
   - Distilled content from all sources is combined
   - GPT-4-turbo creates a comprehensive, structured report addressing the user's query
   - The report is presented in markdown format

## Model Pipeline

Deep Research leverages several AI models for different tasks:

1. **GPT-3.5-Turbo**:
   - Used for query enhancement
   - Optimizes search terms for relevance and recency

2. **GPT-4-Turbo**:
   - Primary model for content analysis
   - Performs information distillation from raw article content

3. **OpenAI o1**:
   - Generates comprehensive reports from distilled information

The models are configured with appropriate parameters:
- Lower temperature (0.3) for factual distillation
- Moderate temperature (0.5) for report generation
- Specific system prompts to guide model behavior for each task

## Data Sources

The current implementation uses Google Search as its primary data source, with the option to modify or extend to include additional sources. We're interested in exploring more specialized data sources to enhance the quality and breadth of information.

### Potential Additional Data Sources

We're considering integrating the following:
- Academic databases
- Industry-specific news sources
- Government data repositories
- Specialized search engines

**Question for Contributors**: Do you have suggestions for additional data sources that would enhance the application's research capabilities? We're particularly interested in APIs or services that provide access to specialized information domains.

## Ethical Considerations

Please review our [Ethics Statement](ETHICS.md) for information on our approach to responsible web scraping, AI use, and data handling.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Deployed App

You can find the Deep learning version of the deep-research app (with content distillation) deployed [here](https://deep-research-cyydabns6j5atynhqxetsk.streamlit.app/)
You can find the Naive version of the deep-research app (without content distillation) deployed [here](https://deep-research-naive-develop.streamlit.app/)