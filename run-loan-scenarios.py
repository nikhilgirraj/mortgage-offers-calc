# Author: Nikhil

def calculate_emi_tiered(principal, rate_periods):
    """
    Calculate EMI payments for tiered interest rates where EMI is based on remaining tenure.

    :param principal: Initial loan amount
    :param rate_periods: List of tuples [(rate1, years1), (rate2, years2), ...]
    :return: List of dicts with EMI info for each period
    """
    results = []
    total_months_remaining = sum(years for _, years in rate_periods) * 12
    start_year = 0

    for rate, years in rate_periods:
        months_in_tier = years * 12
        monthly_rate = rate / (12 * 100)

        # EMI calculated using remaining principal and remaining total months
        installment = (principal * monthly_rate * (1 + monthly_rate) ** total_months_remaining) / \
              ((1 + monthly_rate) ** total_months_remaining - 1)

        total_payment = 0
        interest_paid = 0

        for _ in range(months_in_tier):
            interest = principal * monthly_rate
            principal_payment = installment - interest
            principal -= principal_payment
            interest_paid += interest
            total_payment += installment
            total_months_remaining -= 1

        results.append({
            "period": f"Year {start_year + 1} to {start_year + years}",
            "installment": round(installment, 2),
            "total_paid": round(total_payment, 2),
            "interest_paid": round(interest_paid, 2),
            "ending_balance": round(principal, 2)
        })

        start_year += years

    return results


def run_tiered_loan_scenario(principal, rate_periods):
    """
    Run and display tiered loan scenario results.

    :param principal: Loan amount (e.g. 500000)
    :param rate_periods: List of tuples [(rate%, years), ...]
    """
    schedule = calculate_emi_tiered(principal, rate_periods)
    total_paid_all = 0

    tiers_str = ", then ".join([f"{rate}% for {years} year{'s' if years > 1 else ''}" for rate, years in rate_periods])
    print(f"\nScenario for Loan: €{principal} with rates: {tiers_str}")

    print("------------------------------------------------------------")
    for period in schedule:
        print(f"{period['period']}: Installment = €{period['installment']}, "
              f"Total Paid in Period = €{period['total_paid']}, "
              f"Interest Paid = €{period['interest_paid']}, "
              f"Balance Left = €{period['ending_balance']}")
        total_paid_all += period['total_paid']

    print(f"\nTotal Paid Over All Installments: €{round(total_paid_all, 2)}\n")
    
    
