from pydantic import BaseModel, Field
import agenta as ag
from agenta.sdk.types import MCField
from agenta.sdk.assets import supported_llm_models
from openai import OpenAI
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

# Initialize Agenta
ag.init()

# Instrument OpenAI for tracing
OpenAIInstrumentor().instrument()

# Initialize OpenAI client
client = OpenAI()

# Define the default system prompt
default_system_prompt = """
You are an expert instruction-following AI assistant.
You will be provided with some text and a set of instructions.
Your task is to carefully execute the instructions on the provided text.
Return only the final result.
"""


class Config(BaseModel):
    system_prompt: str = Field(default=default_system_prompt)
    model: str = MCField(default="gpt-3.5-turbo", choices=supported_llm_models)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1, le=4096)


@ag.route("/", config_schema=Config)
@ag.instrument()
def execute_instruction(text: str, instructions: str):
    """
    Executes a set of instructions on the provided text using an LLM.

    Args:
        text (str): The input text to be processed.
        instructions (str): The instructions to execute on the text.

    Returns:
        str: The result of executing the instructions.
    """
    # Retrieve configuration
    config = ag.ConfigManager.get_from_route(Config)

    # Format the user prompt
    user_prompt = f"Instructions:\n{instructions}\n\nText:\n{text}"

    # Call the LLM
    completion = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": config.system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )

    # Return the response content
    return completion.choices[0].message.content


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "agenta.sdk.decorators.routing:app", host="0.0.0.0", port=8000, reload=True
    )
