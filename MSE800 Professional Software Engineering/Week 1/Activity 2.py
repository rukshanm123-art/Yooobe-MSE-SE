

#Input
hours_worked = float(input("Enter hours worked: "))
hourly_rate = float(input("Enter hourly pay rate: "))

#Processing
gross_income = hours_worked * hourly_rate
print("Gross Income: $", round(gross_income, 2))


#Tax Calculation
income = gross_income  #using the gross pay as income

if income <= 15600:
    tax = income * 0.105

elif income <= 53500:
    tax = (income - 15600) * 0.175 + 15600 * 0.105

elif income <= 78100:
    tax = (income - 53500) * 0.30 \
          + (53500 - 15600) * 0.175 \
          + 15600 * 0.105

elif income <= 180000:
    tax = (income - 78100) * 0.33 \
          + (78100 - 53500) * 0.30 \
          + (53500 - 15600) * 0.175 \
          + 15600 * 0.105

else:
    tax = (income - 180000) * 0.39 \
          + (180000 - 78100) * 0.33 \
          + (78100 - 53500) * 0.30 \
          + (53500 - 15600) * 0.175 \
          + 15600 * 0.105

final_income = income - tax

# Output
print("Tax Deducted: $", round(tax, 2))
print("Final Income After Tax: $", round(final_income, 2))
