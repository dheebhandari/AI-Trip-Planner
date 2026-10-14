import re

def extract_float(value) -> float:
    """
    Extract numeric value from strings like:
    '3500 INR', '₹3500', '$120.50', '1000 rs', 'about 300'
    """
    if isinstance(value, (int, float)):
        return float(value)

    match = re.search(r"[-+]?\d*\.?\d+", str(value))
    if not match:
        raise ValueError(f"Could not extract number from: {value}")

    return float(match.group())
