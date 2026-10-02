import requests
import json
from datetime import datetime
#from langchain.tools import tool

from langchain_core.tools import tool

import math
from langchain_experimental.utilities import PythonREPL

python_repl = PythonREPL(
    _locals={
        "math": math
    }
) #To resolve the issue  The 'math' module is not defined.

#python_repl = PythonREPL() #creating instance to reuse across tool calls

#Tool 1
#Calculator Tool

@tool
def calculator_tool(expression: str) -> str:
    """
    Perform mathematical calculation using Python.

    Use this tool is user asks to perform arithmetic or mathematical calculations.
    Supports arithmetic, trigonometric functions, logarithms,
    factorials, square roots, powers, and mathematical constants.

    Examples:
        math.factorial(10)
        math.sin(math.radians(30))
        math.cos(math.radians(60))
        math.log10(100)
        math.log(10)
        math.sqrt(25)
        2**10
        math.pi * 5**2

    TRIGONOMETRIC FUNCTIONS:
        - Assume angles are in DEGREES by default.
        - If the user explicitly says radians, use radians.
        - Convert degrees to radians using math.radians() before
        passing the value to math.sin(), math.cos(), or math.tan().

    FACTORIAL:
        - "10 factorial"
        -> math.factorial(10)

    Args: 
        A valid Python mathematical expression

    Returns: 
        JSON string containing the expression and result,
        or an error message.

    """
    try:
        #result = python_repl.run(
        #    f"print({expression})"
        #) #Returning resul tin json format instead of String
        result = python_repl.run(
            f"print({expression})"
        )

        return json.dumps({
            "expression": expression,
            "result": result.strip()
        })

    except Exception as e:
        #return f"Error calculating expression: {e}"
        return json.dumps({
            "expression": expression,
            "error": f"Error calculating expression: {str(e)}"
        })

#Tool 2
#EMI Calculator Tool

@tool
def emi_calculator_tool(
    loan_amount: float,
    interest_rate: float,
    tenure_months: int,
    interest_rate_period: str = "annual",
) -> str:
    """
    Calculate EMI based on formula:
    EMI = P × r × (1+r)^n / ((1+r)^n - 1)
    Where:
    P = Loan Amount
    r = Monthly Interest Rate
    n = Number of Months

    Args:
        loan_amount:
            Principal loan amount.

        interest_rate:
            Interest rate in percentage.
            Example: 8.5 means 8.5%.

        tenure_months:
            Loan tenure in months.

        interest_rate_period:
            Specifies whether the interest rate is annual or monthly.
            Accepted values:
                - "annual"
                - "monthly"

            Defaults to "annual".

    Returns:
        A JSON string containing monthly EMI, total payment,
        and total interest.

    """

    try:
        # Validate inputs

        if loan_amount <= 0:
            return json.dumps({
                "error": "Loan amount must be greater than 0."
            })

        if interest_rate < 0:
            return json.dumps({
                "error": "Interest rate cannot be negative."
            })

        if tenure_months <= 0:
            return json.dumps({
                "error": "Tenure must be greater than 0 months."
            })

        # Normalize rate period

        rate_period = interest_rate_period.lower().strip()

        # Convert interest rate

        if rate_period in [
            "annual",
            "yearly",
            "per annum",
            "pa",
            "p.a.",
        ]:
            # Annual percentage → monthly decimal

            r = interest_rate / 12 / 100

        elif rate_period in [
            "monthly",
            "per month",
            "pm",
            "p.m.",
        ]:
            # Monthly percentage → monthly decimal

            r = interest_rate / 100

        else:
            return json.dumps({
                "error": (
                    "Invalid interest rate period. "
                    "Use 'annual' or 'monthly'."
                )
            })

        # Calculate EMI

        P = loan_amount
        n = tenure_months

        # Special case: 0% interest
        if r == 0:
            emi = P / n

        else:
            emi = (
                P * r * (1 + r) ** n
                / ((1 + r) ** n - 1)
            )

        # Calculate totals

        total_payment = emi * n
        total_interest = total_payment - P

        # Return JSON

        return json.dumps({
            "monthly_emi": round(emi, 2),
            "loan_amount": round(P, 2),
            "interest_rate": round(interest_rate, 2),
            "interest_rate_period": rate_period,
            "tenure_months": n,
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2)
        })

    except Exception as e:
        return json.dumps({
            "error": f"Error calculating EMI: {str(e)}"
        })
    
        #Not using String format
        # Return result
        #return (
        #    f"Monthly EMI: ₹{emi:,.2f}\n"
        #    f"Loan Amount: ₹{P:,.2f}\n"
        #    f"Interest Rate: {interest_rate:.2f}% "
        #    f"({rate_period})\n"
        #    f"Tenure: {n} months\n"
        #    f"Total Payment: ₹{total_payment:,.2f}\n"
        #    f"Total Interest: ₹{total_interest:,.2f}"
        #)


    #except Exception as e:
    #    return f"Error calculating EMI: {e}"

#Tool 3
#SIP Investment Calculator

@tool
def sip_calculator_tool(
    monthly_investment: float,
    interest_rate: float,
    tenure_months: int,
    interest_rate_period: str = "annual",
) -> str:
    """
    Calculate future value of monthly investments based on below formula:

        FV = P × ((1+r)^n - 1) / r

    Where:
        P = Monthly Investment
        r = Monthly Return as a decimal
        n = Total Months

    Args:
        monthly_investment:
            Amount invested every month.

        interest_rate:
            Expected return rate as a percentage.
            Example:
                12 = 12% annual return
                1 = 1% monthly return

        tenure_months:
            Total investment period in months.

        interest_rate_period:
            Specifies whether the return rate is annual or monthly.
            Accepted values:
                - "annual"
                - "monthly"

            Defaults to "annual".

    Returns:
        JSON string containing total investment,
        estimated returns, and future value.
    """
    try:
        # Validate inputs

        if monthly_investment <= 0:
            return json.dumps({
                "error": "Monthly investment must be greater than 0."
            })

        if interest_rate < 0:
            return json.dumps({
                "error": "Interest rate cannot be negative."
            })

        if tenure_months <= 0:
            return json.dumps({
                "error": "Tenure must be greater than 0 months."
            })

        # Convert interest rate

        rate_period = interest_rate_period.lower().strip()

        if rate_period in [
            "annual",
            "yearly",
            "per annum",
            "pa",
            "p.a.",
        ]:
            # Annual rate → monthly rate
            r = interest_rate / 12 / 100

        elif rate_period in [
            "monthly",
            "per month",
            "pm",
            "p.m.",
        ]:
            # Monthly rate → decimal
            r = interest_rate / 100

        else:
            return json.dumps({
                "error": (
                    "Invalid interest rate period. "
                    "Use 'annual' or 'monthly'."
                )
            })

        P = monthly_investment
        n = tenure_months

        # Calculate Future Value

        if r == 0:
            future_value = P * n
        else:
            future_value = (
                P * ((1 + r) ** n - 1) / r
            )

        # Calculate investment details

        total_investment = P * n
        estimated_returns = future_value - total_investment

        # Return result as JSON

        return json.dumps({
            "monthly_investment": round(P, 2),
            "interest_rate": round(interest_rate, 2),
            "interest_rate_period": rate_period,
            "tenure_months": n,
            "total_investment": round(total_investment, 2),
            "estimated_returns": round(estimated_returns, 2),
            "future_value": round(future_value, 2)
        })

    except Exception as e:
        return json.dumps({
            "error": f"Error calculating SIP: {str(e)}"
        })

    
        # Return result in string format

        #return (
        #    f"Monthly Investment: ₹{P:,.2f}\n"
        #    f"Interest Rate: {interest_rate:.2f}% "
        #    f"({rate_period})\n"
        #    f"Tenure: {n} months\n"
        #    f"Total Investment: ₹{total_investment:,.2f}\n"
        #    f"Estimated Returns: ₹{estimated_returns:,.2f}\n"
        #    f"Future Value: ₹{future_value:,.2f}"
        #)

        
    #except Exception as e:
    #    return f"Error calculating SIP: {e}"

#Tool 4
#Budget Planner Tool

@tool
def budget_planner_tool(monthly_income: float) -> str:
    """
    Plan monthly budget allocation based on monthly income using the 50-30-20 rule.

    The 50-30-20 rule allocates:
        - 50% to Needs
        - 30% to Wants
        - 20% to Savings

    Args:
        monthly_income:
            Monthly take-home income available for budgeting.

    Returns:
        A JSON string containing the recommended allocation
        for needs, wants, savings, and the total income.
    """
    try:
        # Validate input
        if monthly_income <= 0:
            return json.dumps({
                "error": "Monthly income must be greater than 0."
            })
        # Allocation Calculation

        needs_percentage = 50
        wants_percentage = 30
        savings_percentage = 20

        needs_amount = monthly_income * (needs_percentage/100)
        wants_amount = monthly_income * (wants_percentage/100)
        savings_amount = monthly_income * (savings_percentage/100)

        # Return result as JSON

        return json.dumps({
            "monthly_income": round(monthly_income, 2),

            "needs": {
                "percentage": needs_percentage,
                "amount": round(needs_amount, 2)
            },

            "wants": {
                "percentage": wants_percentage,
                "amount": round(wants_amount, 2)
            },

            "savings": {
                "percentage": savings_percentage,
                "amount": round(savings_amount, 2)
            },

            "total_allocated": round(
                needs_amount + wants_amount + savings_amount,
                2
            )
        })

    except Exception as e:
        return json.dumps({
            "error": f"Error calculating budget: {str(e)}"
        })

    



