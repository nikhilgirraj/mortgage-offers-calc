def calculate_emi_tiered(principal, rate_periods):
    total_months_remaining = sum(tier['years'] for tier in rate_periods) * 12
    start_year = 0
    results = []

    for tier in rate_periods:
        rate = tier['rate']
        years = tier['years']
        months_in_tier = years * 12
        monthly_rate = rate / (12 * 100)

        emi = (principal * monthly_rate * (1 + monthly_rate) ** total_months_remaining) / \
              ((1 + monthly_rate) ** total_months_remaining - 1)

        total_payment = 0
        interest_paid = 0

        for _ in range(months_in_tier):
            interest = principal * monthly_rate
            principal_payment = emi - interest
            principal -= principal_payment
            interest_paid += interest
            total_payment += emi
            total_months_remaining -= 1

        results.append({
            "period": f"Year {start_year + 1} to {start_year + years}",
            "installment": round(emi, 2),
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

    # Format tier info nicely
    def tier_str(tier):
        return f"{tier['rate']}% for {tier['years']} year{'s' if tier['years'] > 1 else ''}"

    tiers_description = ", then ".join([tier_str(t) for t in rate_periods])
    print(f"\nScenario for Loan: €{principal} with rates: {tiers_description}")
    print("------------------------------------------------------------")

    for period in schedule:
        print(f"{period['period']}: Installment = €{period['installment']}, "
              f"Total Paid in Period = €{period['total_paid']}, "
              f"Interest Paid = €{period['interest_paid']}, "
              f"Balance Left = €{period['ending_balance']}")
        total_paid_all += period['total_paid']

    print(f"\nTotal Paid Over All Installments: €{round(total_paid_all, 2)}\n")

