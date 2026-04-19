# Instruction Executor Workflow

This is an example of an Agenta Custom Workflow that takes a piece of `text` and a set of `instructions`, and executes those instructions on the text using an LLM.

## Features
- Utilizes the OpenAI API for instruction execution.
- Configurable system prompt, model choice, temperature, and max tokens.
- Instrumented with OpenTelemetry for tracing.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Copy `.env.example` to `.env` and add your OpenAI API key.
   ```bash
   cp .env.example .env
   # Edit .env and set OPENAI_API_KEY
   ```

## Running the Application

You can serve the application locally using the Agenta CLI:
```bash
agenta serve app.py
```

Or you can run it directly with Python:
```bash
python app.py
```

The application will be available at `http://localhost:8000` and can be interacted with via the Agenta platform or API.
