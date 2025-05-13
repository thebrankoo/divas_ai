# Python Project with OpenAI Integration

A simple Python project that demonstrates integration with the OpenAI API.

## Setup

1. Clone the repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Alternatively, set it as an environment variable directly

## Usage

Run the main script:
```bash
python src/main.py
```

This will:
1. Load environment variables from the `.env` file
2. Check if the OpenAI API key is configured
3. Send a sample prompt to OpenAI
4. Display the response

## OpenAI Module

The project includes a simple OpenAI module with the following features:
- `OpenAIClient`: A client for interacting with OpenAI APIs
- Basic error handling
- Environment variable support
- Chat completion functionality 