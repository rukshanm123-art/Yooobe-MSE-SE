import math


def rect_to_polar():
    print("\n--- Rectangular (a + bi) -> Polar (r, Q) ---")
    try:
        real = float(input("Enter Real number (a): "))
        imag = float(input("Enter Imaginary number (i): "))

        #Calculate Magnitude (r)
        r = math.sqrt(real ** 2 + imag ** 2)

        #Calculate Angle (theta)
        theta_rad = math.atan2(imag, real)
        theta_deg = math.degrees(theta_rad)

        print(f"\nResult:")
        print(f"Magnitude (r): {r:.4f}")
        print(f"Angle (Q): {theta_deg:.2f}° ({theta_rad:.4f} rad)")

    except ValueError:
        print("Invalid input. Please enter numbers.")


def polar_to_rect():
    print("\n--- Polar (r, Q) -> Rectangular (a + bi) ---")
    try:
        r = float(input("Enter Magnitude (r): "))
        deg = float(input("Enter Angle (Q) in degrees: "))

        #Convert to radians for calculation
        rad = math.radians(deg)

        #Calculate a and b
        a = r * math.cos(rad)
        b = r * math.sin(rad)

        #Clean up floating point errors (e.g. cos(90) -> 0)
        if abs(a) < 1e-10: a = 0.0
        if abs(b) < 1e-10: b = 0.0

        sign = "+" if b >= 0 else "-"
        print(f"\nResult:")
        print(f"{a:.3f} {sign} {abs(b):.3f}i")

    except ValueError:
        print("Invalid input. Please enter numbers.")


def main():
    while True:
        print("\n=== Complex Number Converter ===")
        print("1. Rectangular -> Polar")
        print("2. Polar -> Rectangular")
        print("3. Exit")

        choice = input("Select mode (1-3): ")

        if choice == '1':
            rect_to_polar()
        elif choice == '2':
            polar_to_rect()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()