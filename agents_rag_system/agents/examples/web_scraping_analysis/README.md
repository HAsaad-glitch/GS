# Web Scraping Analysis Agent

## Overview

The Web Scraping Analysis Agent evaluates websites to determine the most effective scraping techniques and identifies potential challenges like CAPTCHA systems and anti-bot measures. It provides comprehensive scraping strategies tailored to the specific website's structure and protection mechanisms.

## Features

- **Website Structure Analysis:** Detects dynamic content, JavaScript frameworks, AJAX calls, infinite scrolling, and form submissions.
- **Anti-scraping Measure Detection:** Identifies the presence of CAPTCHAs, rate limiting, and IP blocking mechanisms.
- **Website Tree Extraction:** Creates a simplified representation of the website's DOM structure.
- **Intelligent Recommendations:** Suggests appropriate scraping tools and techniques based on website analysis.
- **Scraping Strategy Generation:** Provides a detailed step-by-step strategy for scraping the target website.

## Usage

### Basic Usage

```python
from GS.agents_rag_system.config.config import AgentConfig
from GS.agents_rag_system.agents.examples.web_scraping_analysis.agent import WebScrapingAnalysisAgent

# Initialize the agent
config = AgentConfig()
agent = WebScrapingAnalysisAgent(config)

# Analyze a website
result = agent.process_website("https://example.com")

# Print the recommended scraping techniques
print("Recommended Scraping Techniques:")
for technique in result["recommendations"]:
    print(f"- {technique}")

# Print the scraping strategy
print("\nScraping Strategy:")
print(result["scraping_strategy"])
```

### Chat Interface

```python
# Chat with the agent about web scraping
response = agent.chat("How can I handle CAPTCHA when scraping e-commerce websites?")
print(response)

# Process specific queries
answer = agent.process_query("What's the best way to scrape JavaScript-heavy websites?")
print(answer)
```

## Configuration Options

The agent supports the following configuration options:

- `use_proxies` (bool): Whether to consider proxy usage in the analysis (default: True)
- `detect_captcha` (bool): Whether to check for CAPTCHA presence (default: True)

## Response Structure

The `process_website` method returns a dictionary with the following keys:

- `analysis`: Detailed analysis of website features and structure
- `proxy_captcha_info`: Information about proxy requirements and CAPTCHA detection
- `website_tree_summary`: A simplified representation of the website's DOM structure
- `recommendations`: List of recommended scraping techniques and tools
- `scraping_strategy`: A comprehensive strategy for scraping the website

## Requirements

- Python 3.7+
- BeautifulSoup
- Requests
- Access to LLM and RAG services via the agent system

## Example

Analyzing an e-commerce website:

```python
result = agent.process_website("https://www.amazon.com")

# Result includes:
# - Detection of dynamic content, AJAX calls
# - Identification of CAPTCHA systems
# - Recommendations for using Selenium with proxy rotation
# - A detailed scraping strategy with error handling
``` 