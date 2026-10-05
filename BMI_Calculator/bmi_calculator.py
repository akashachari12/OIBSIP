print("================================")
print("        BMI CALCULATOR")
print("================================")

try:
    weight = float(input("Enter your weight in kg: "))
    height = float(input("Enter your height in meters: "))

    if weight <= 0 or height <= 0:
        print("\nPlease enter valid positive values.")

    else:
        bmi = weight / (height * height)

        print("\n--------------------------------")
        print("Your BMI is:", round(bmi, 2))

        if bmi < 18.5:
            category = "Underweight"
            message = "You may need to gain some weight."

        elif bmi < 25:
            category = "Normal weight"
            message = "Your weight is in the normal range."

        elif bmi < 30:
            category = "Overweight"
            message = "You may need to focus on a healthy lifestyle."

        else:
            category = "Obesity"
            message = "Consider focusing on a healthy lifestyle."

        print("Category:", category)
        print("Message:", message)
        print("--------------------------------")

except ValueError:
    print("\nPlease enter numbers only.")