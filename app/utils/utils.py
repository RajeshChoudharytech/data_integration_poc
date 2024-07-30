import logging
from typing import Any, Dict, Union


logger = logging.getLogger(__name__)

# Helper function to convert all text fields in a dict to uppercase
def convert_to_uppercase(data: Union[Dict[str, Any], list]) -> Union[Dict[str, Any], list]:
    """
    Convert all text fields in a dictionary or list to uppercase.

    Args:
        data (Union[Dict[str, Any], list]): The data to be converted.

    Returns:
        Union[Dict[str, Any], list]: The converted data.
    """
    # Check if the data is a dictionary
    if isinstance(data, dict):
        # Convert all text fields to uppercase
        return {k: (v.upper() if isinstance(v, str) else v) for k, v in data.items()}
    # Check if the data is a list
    elif isinstance(data, list):
        # Recursively convert all text fields in the list
        return [convert_to_uppercase(item) for item in data]
    # If the data is neither a dictionary nor a list, return it as is
    return data
