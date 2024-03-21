from datetime import datetime
# Import Investement inside the methods if needed

class FinancialProjector:
    @staticmethod
    def calculate_projected_historical_annual_interest_rate(investment):
        # If type hints are needed, consider importing inside the method or using 'from typing import TYPE_CHECKING' with 'if TYPE_CHECKING:'
        from investements import Investement  # Move the import here if it's necessary for type hints  # noqa: F401

        # If an annual interest rate is already provided, use it to calculate the annual interest rate
        if investment.provided_annual_interest_rate != 0:
            return investment.provided_annual_interest_rate

        # Calculate the number of months between the initial investment date and the last update date
        date_format = "%d-%m-%Y"
        initial_date = datetime.strptime(investment.itd_date, date_format)
        current_date = datetime.strptime(investment.last_update_date, date_format)
        delta = current_date - initial_date
        n_months = max(delta.days / 30, 1)  # Ensure at least 1 month to avoid division by zero

        # Calculate the monthly interest rate using the formula derived from the compound interest formula
        if investment.normalized_initial_investment != 0:  # Avoid division by zero
            r = (investment.normalized_amount / investment.normalized_initial_investment) ** (1 / n_months) - 1
        else:
            return 0  # Return 0 if initial investment is 0 to avoid division by zero

        # Annualize the monthly interest rate
        annualized_rate = (1 + r) ** 12 - 1

        return annualized_rate * 100  # Convert to percentile

    def calculate_future_compounded_value(self, investment, years: int, annual_interest_rate: float):
        from investements import Investement  # Import here if necessary for type hints  # noqa: F401

        # Check if the annual interest rate is zero and raise an exception if so
        if annual_interest_rate == 0:
            raise ValueError("Annual interest rate must be non-zero.")

        # Calculate the future value using the compound interest formula: A = P(1 + r)^n
        future_value = investment.normalized_amount * (1 + annual_interest_rate) ** years

        return future_value
