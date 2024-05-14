# Standard Library
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique id

    Returns:
        str: generated id without hyphen
    """
    return str(uuid4()).replace("-", "")
