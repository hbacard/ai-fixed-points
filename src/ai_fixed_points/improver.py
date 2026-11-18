from .base import BaseAgent


class CodeImprover(BaseAgent):
    """Improve code as a highly skilled engineer."""

    prompt_file = "improve.md"
    output_type = str
