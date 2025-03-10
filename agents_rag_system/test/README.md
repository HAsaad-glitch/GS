# Test Directory

This directory contains test scripts for the Multi-Agent RAG System. These tests validate the functionality of various components and agents in the system.

## Test Files

- `test.py`: Comprehensive test script for the RAG system with OpenAI integration
- `test_agent.py`: Tests for the ResearchAgent functionality
- `test_agent2.py`: Additional agent tests
- `test_agent3.py`: Additional agent tests
- `test_agent4.py`: Additional agent tests

## Running Tests

### Prerequisites

Before running the tests, make sure you have:

1. Set up the required environment variables in a `.env` file or in your environment
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key (if testing Anthropic models)
   CHROMA_HOST=localhost (optional, for HTTP client tests)
   CHROMA_PORT=8000 (optional, for HTTP client tests)
   ```

2. Installed all dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Running All Tests

To run all tests:

```bash
cd agents_rag_system
python -m test.test
```

### Running Specific Tests

To run a specific test file:

```bash
cd agents_rag_system
python -m test.test_agent
```

## Test Coverage

The tests cover the following functionality:

### RAG System Tests (`test.py`)

- ChromaDB vector store integration (both HTTP and local clients)
- Document embedding and retrieval
- Query processing and response generation
- Full RAG pipeline with OpenAI models

### Agent Tests (`test_agent.py`, etc.)

- Research agent functionality
- Document summarization
- Chat capabilities
- Query processing
- Agent-specific features

## Adding New Tests

When adding new tests:

1. Create a new test file following the naming convention `test_*.py`
2. Import the necessary components from the system
3. Structure your tests with clear sections and print statements for debugging
4. Include setup and teardown steps (e.g., creating and deleting test collections)
5. Add appropriate error handling and validation

## Test Output

The test scripts provide detailed output about each step of the testing process, including:

- Configuration setup
- Document processing
- Query execution
- Response generation
- Performance metrics

If a test fails, it will display an error message indicating the specific failure point.

## Troubleshooting

Common issues when running tests:

1. **Missing API Keys**: Ensure all required API keys are set in your environment
2. **ChromaDB Connection Issues**: If using HTTP client, verify ChromaDB is running and accessible
3. **Import Errors**: Make sure the system path is correctly set up for imports
4. **Memory Issues**: Some tests may require significant memory, especially with large document collections

For any persistent issues, check the error messages and refer to the relevant component documentation. 