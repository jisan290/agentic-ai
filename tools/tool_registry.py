from .calculator import calculate
from .text_analyzer import count_words
from .pdf_reader import read_pdf
from .docx_reader import read_docx
from .web_search import web_search


TOOL_FUNCTIONS = {
    "calculate": calculate,
    "read_docx": read_docx,
    "count_words": count_words,
    "read_pdf": read_pdf,
    "web_search": web_search,
}


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "calculate",
        "description": "Calculate a mathematical expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A mathematical expression such as 25 * 8",
                }
            },
            "required": ["expression"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "count_words",
        "description": "Count the number of words in a piece of text.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text whose words should be counted.",
                }
            },
            "required": ["text"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "read_pdf",
        "description": "Read the text content of a PDF file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the PDF file to be read.",
                }
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    
    {
        "type": "function",
        "name": "read_docx",
        "description": "Read and extract text from a DOCX file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the DOCX file to be read.",
                }
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "web_search",
        "description": (
            "Search the web using Google and return the top results. "
            "Use this when the user asks a question that requires "
            "up-to-date information, facts you are unsure about, or "
            "any topic that would benefit from online research."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up.",
                },
                "num_results": {
                    "type": "integer",
                    "description": (
                        "Number of results to return (1-10). "
                        "Defaults to 5."
                    ),
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

RESEARCH_TOOLS = TOOL_DEFINITIONS