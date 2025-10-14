"""
Calculator and utility tools
"""
import math
import re
from typing import Any, Dict
from datetime import datetime, timedelta


class Calculator:
    """Perform calculations and conversions"""
    
    @staticmethod
    def evaluate(expression: str) -> Dict[str, Any]:
        """Safely evaluate mathematical expression"""
        try:
            # Remove any non-math characters for safety
            safe_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            
            # Allowed functions
            allowed_names = {
                'sqrt': math.sqrt,
                'pow': math.pow,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'exp': math.exp,
                'abs': abs,
                'round': round,
                'pi': math.pi,
                'e': math.e,
            }
            
            # Evaluate
            result = eval(safe_expr, {"__builtins__": {}}, allowed_names)
            
            return {
                'success': True,
                'result': result,
                'error': None
            }
        
        except Exception as e:
            return {
                'success': False,
                'result': None,
                'error': str(e)
            }
    
    @staticmethod
    def percentage(value: float, percentage: float) -> float:
        """Calculate percentage of a value"""
        return (value * percentage) / 100
    
    @staticmethod
    def compound_interest(
        principal: float,
        rate: float,
        time: float,
        compounds_per_year: int = 1
    ) -> float:
        """Calculate compound interest"""
        return principal * (1 + rate / (100 * compounds_per_year)) ** (compounds_per_year * time)
    
    @staticmethod
    def npv(rate: float, cash_flows: list) -> float:
        """Calculate Net Present Value"""
        npv = 0
        for i, cash_flow in enumerate(cash_flows):
            npv += cash_flow / (1 + rate) ** i
        return npv
    
    @staticmethod
    def roi(gain: float, cost: float) -> float:
        """Calculate Return on Investment"""
        return ((gain - cost) / cost) * 100


# Global instance
calculator = Calculator()

