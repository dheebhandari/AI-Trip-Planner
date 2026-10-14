import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper

from utils.number_parser import extract_float

load_dotenv()


@tool
def multiply(a, b) -> float:
    """
    Multiply two numbers (LLM-safe).
    Accepts inputs like '5', '5 days', '₹2000', etc.
    """
    return extract_float(a) * extract_float(b)


@tool
def add(a, b) -> float:
    """
    Add two numbers (LLM-safe).
    """
    return extract_float(a) + extract_float(b)


@tool
def currency_converter(from_curr: str, to_curr: str, value) -> float:
    """
    Convert currency using Alpha Vantage.
    """

    amount = extract_float(value)

    os.environ["ALPHAVANTAGE_API_KEY"] = os.getenv("ALPHAVANTAGE_API_KEY")
    alpha_vantage = AlphaVantageAPIWrapper()

    response = alpha_vantage._get_exchange_rate(from_curr, to_curr)
    exchange_rate = float(
        response["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    )

    return amount * exchange_rate
