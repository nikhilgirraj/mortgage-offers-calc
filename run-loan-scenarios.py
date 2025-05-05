def calculate_emi_tiered(principal, rate_periods):
    total_months_remaining = sum(tier['years'] for tier in rate_periods) * 12
    start_year = 0
    results = []

    for tier in rate_periods:
        rate = tier['rate']
        years = tier['years']
        months_in_tier = years * 12
        monthly_rate = rate / (12 * 100)

        # Handle lump sum repayment at the beginning of this tier
        lump_sum = tier.get('lump_sum', 0)
        principal -= lump_sum

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

        # Cashback info is just for reporting (not affecting calculation)
        cashback = tier.get('cashback', 0)

        results.append({
            "period": f"Year {start_year + 1} to {start_year + years}",
            "installment": round(emi, 2),
            "total_paid": round(total_payment, 2),
            "interest_paid": round(interest_paid, 2),
            "ending_balance": round(principal, 2),
            "cashback": cashback
        })

        start_year += years

    return results

import pandas as pd

def run_tiered_loan_scenario(principal, rate_periods):
    schedule = calculate_emi_tiered(principal, rate_periods)
    total_paid_all = 0
    total_cashback = 0
    total_years = sum(tier['years'] for tier in rate_periods)

    data_rows = []

    for idx, period in enumerate(schedule):
        tier = rate_periods[idx]
        months = tier['years'] * 12

        effective = None
        if period['cashback']:
            effective = (period['total_paid'] - period['cashback']) / months

        data_rows.append({
            "Period": period['period'],
            "Rate (%)": tier['rate'],
            "Installment (€)": period['installment'],
            "Effective Installment (€)": round(effective, 2) if effective else None,
            "Total Paid (€)": period['total_paid'],
            "Interest Paid (€)": period['interest_paid'],
            "Ending Balance (€)": period['ending_balance'],
            "Lump Sum (€)": tier.get('lump_sum', 0.0)
        })

        total_paid_all += period['total_paid']
        total_cashback += period['cashback']

    df = pd.DataFrame(data_rows)

    # Format floats with € symbol where appropriate
    pd.options.display.float_format = lambda x: f"€{x:,.2f}"

    # Description of the tiers
    def tier_str(tier):
        parts = [f"{tier['rate']}% for {tier['years']} year{'s' if tier['years'] > 1 else ''}"]
        if 'cashback' in tier:
            parts.append(f"with €{tier['cashback']} cashback")
        if 'lump_sum' in tier:
            parts.append(f"€{tier['lump_sum']} lump sum")
        return " ".join(parts)

    tiers_description = ", then ".join([tier_str(t) for t in rate_periods])
    print(f"\nScenario for Loan: €{principal} with rates: {tiers_description}\n")

    print(df.to_string(index=False))

    print(f"\nTotal Paid Over All Installments: €{round(total_paid_all, 2)} over {total_years} years")
    if total_cashback > 0:
        print(f"Total Cashback Received:         €{round(total_cashback, 2)}")
        print(f"Net Cost to Borrower:            €{round(total_paid_all - total_cashback, 2)}")
