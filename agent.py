import json
import time
from google.genai import errors
from dotenv import load_dotenv
from google import genai

from tools.tool_registry import (
    TOOL_FUNCTIONS,
    RESEARCH_TOOLS,
)

load_dotenv()

client = genai.Client()

MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7_flash",
]


SYSTEM_INSTRUCTION = """
You are MiniResearcher, a research assistant.

Your job is to investigate questions and provide useful, accurate answers.

Rules:
1. Use read_pdf when the user provides a PDF file path and asks you to inspect, summarize, explain, analyze, or extract information from that PDF.
2. Use calculator when mathematical calculations are needed.
3. Use count_words when counting words is useful.
4. Never pretend that you read a file if the read_pdf tool was not actually used.
5. Do not invent information that is not present in the provided sources or files.
6. Synthesize information instead of simply copying it.
7. Give the user a clear, structured answer.
"""

def create_initial_interaction(question):

    last_error = None

    for model in MODELS:

        for attempt in range(3):

            try:
                interaction = client.interactions.create(
                    model=model,
                    system_instruction=SYSTEM_INSTRUCTION,
                    input=question,
                    tools=RESEARCH_TOOLS,
                )

                print(f"[MiniResearcher] Using model: {model}")

                return interaction, model

            except errors.APIError as e:

                last_error = e

                if e.code in (500, 502, 503, 504):
                    delay = 2 ** attempt

                    print(
                        f"[MiniResearcher] {model} is temporarily unavailable."
                    )
                    print(
                        f"[MiniResearcher] Retry {attempt + 1}/3 "
                        f"after {delay} seconds..."
                    )

                    time.sleep(delay)
                    continue

                if e.code == 429:
                    print(
                        f"[MiniResearcher] {model} hit a quota/rate limit."
                    )
                    break

                raise

    raise last_error


def run_agent(question):

    interaction, model = create_initial_interaction(question)

    while True:

        function_results = []

        for step in interaction.steps:

            if step.type != "function_call":
                continue

            tool_name = step.name
            arguments = step.arguments

            if tool_name not in TOOL_FUNCTIONS:
                raise ValueError(
                    f"Unknown tool requested by model: {tool_name}"
                )

            tool_function = TOOL_FUNCTIONS[tool_name]

            result = tool_function(**arguments)

            function_results.append(
                {
                    "type": "function_result",
                    "name": tool_name,
                    "call_id": step.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(result),
                        }
                    ],
                }
            )

        if not function_results:
            return interaction.output_text

        interaction = client.interactions.create(
            model=model,
            previous_interaction_id=interaction.id,
            input=function_results,
            tools=RESEARCH_TOOLS,
        )