# from utils.expense_calculator import Calculator
# from typing import List
# from langchain.tools import tool

# class CalculatorTool:
#     def __init__(self):
#         self.calculator = Calculator()
#         self.calculator_tool_list = self._setup_tools()

#     def _setup_tools(self) -> List:
#         """Setup all tools for the calculator tool"""
#         @tool
#         def estimate_total_hotel_cost(price_per_night:str, total_days:float) -> float:
#             """Calculate total hotel cost"""
#             return self.calculator.multiply(price_per_night, total_days)
        
#         @tool
#         def calculate_total_expense(costs: list[float]) -> float:
#             """Calculate total expense of the trip"""
#             return self.calculator.calculate_total(*costs)

#         # def calculate_total_expense(*costs: float) -> float:
#         #     """Calculate total expense of the trip"""
#         #     return self.calculator.calculate_total(*costs)
        
#         @tool
#         def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
#             """Calculate daily expense"""
#             return self.calculator.calculate_daily_budget(total_cost, days)
        
#         return [estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]



from typing import List
from langchain.tools import tool
from utils.expense_calculator import Calculator


class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Set up expense calculation tools."""

        @tool
        def estimate_total_hotel_cost(
            price_per_night: float,
            total_days: int
        ) -> float:
            """Calculate total hotel cost.
            Pass price_per_night and total_days as numeric values.
            Example: price_per_night=1500, total_days=5.
            """
            if price_per_night < 0 or total_days < 0:
                raise ValueError("Price and days cannot be negative.")

            return self.calculator.multiply(
                price_per_night, total_days
            )

        @tool
        def calculate_total_expense(costs: List[float]) -> float:
            """Calculate total trip expenses.

            IMPORTANT: costs must be a JSON array of numbers.
            Calculate all multiplications BEFORE calling this tool.
            Correct: costs=[20000, 7500, 2500, 1500, 1000]
            Incorrect: costs=[20000, 1500*5, 500*5]
            """
            if not costs:
                return 0.0

            if any(cost < 0 for cost in costs):
                raise ValueError("Costs cannot be negative.")

            return self.calculator.calculate_total(*costs)

        @tool
        def calculate_daily_expense_budget(
            total_cost: float,
            days: int
        ) -> float:
            """Calculate the average daily trip budget.
            Pass total_cost and days as numeric values.
            """
            if total_cost < 0:
                raise ValueError("Total cost cannot be negative.")

            if days <= 0:
                raise ValueError("Days must be greater than zero.")

            return self.calculator.calculate_daily_budget(
                total_cost, days
            )

        return [
            estimate_total_hotel_cost,
            calculate_total_expense,
            calculate_daily_expense_budget,
        ]
