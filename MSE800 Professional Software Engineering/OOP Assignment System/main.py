from src.system import RentalSystem
from src.factory import UserFactory


def get_safe_int(prompt: str) -> int:
    """
    Robust integer input handler:
    - Strips spaces
    - Allows '$' symbol (e.g., "$50")
    - Re-prompts until a valid integer is entered
    """
    while True:
        try:
            raw = input(prompt).replace("$", "").strip()
            return int(raw)
        except ValueError:
            print("!!! Input Error: Please enter a numeric value only.")


def main():
    sys = RentalSystem()
    user = None

    while True:
        try:
            #AUTH MENU (NO USER LOGGED IN)
            if not user:
                print("\n=== YOOBEE CAR RENTAL SYSTEM ===")
                ch = input("1. Login\n2. Register\n3. Exit\n> ").strip()

                if ch == "2":
                    #Typo prevention loop for role
                    while True:
                        role = input("Register as (customer/admin): ").lower().strip()
                        if role in ["admin", "customer"]:
                            break
                        print(f"!!! '{role}' is invalid. Use 'admin' or 'customer'.")

                    un = input("Username: ").strip()
                    pw = input("Password: ").strip()
                    sec = input("Admin Secret: ").strip() if role == "admin" else ""

                    try:
                        #Store user in system memory
                        sys.users[un] = UserFactory.create_user(un, pw, role, sec)
                        print("Registration Successful!")
                    except Exception as e:
                        print(f"Error: {e}")

                elif ch == "1":
                    un = input("User: ").strip()
                    pw = input("Pass: ").strip()
                    u = sys.users.get(un)

                    if u and u.check_password(pw):
                        user = u
                        print(f"Login successful. Welcome {user.get_username()}!")
                    else:
                        print("Login Failed.")

                elif ch == "3":
                    print("Exiting... Goodbye!")
                    break
                else:
                    print("!!! Invalid option. Please choose 1, 2, or 3.")


            #USER MENU (LOGGED IN)

            else:
                user.display_menu()
                cmd = input("> ").strip()

                #ADMIN MENU

                if user.role == "Admin":

                    if cmd == "1":  #View Vehicles
                        if not sys.cars:
                            print("\n--- No cars in Vehicles to view ---")
                        else:
                            print("\n--- Vehicles ---")
                            for c in sys.cars:
                                #ONLY CHANGE: clearer output (year, rental range, nice availability text)
                                status = "Available" if c.is_available else "Unavailable"
                                print(
                                    f"[{c.car_id}] {c.make} {c.model} ({c.year}) | "
                                    f"{c.mileage} km | ${c.daily_rate}/day | "
                                    f"Rental: {c.min_days}-{c.max_days} days | {status}"
                                )

                    elif cmd == "2":  #Add Car
                        make = input("Make: ").strip()
                        model = input("Model: ").strip()
                        year = get_safe_int("Year: ")
                        mileage = get_safe_int("Mileage: ")
                        rate = get_safe_int("Rate ($/day): ")
                        min_days = get_safe_int("Min Days: ")
                        max_days = get_safe_int("Max Days: ")

                        print(sys.add_car(make, model, year, mileage, rate, min_days, max_days))

                    elif cmd == "3":  #Update Car Mileage
                        car_id = get_safe_int("Car ID: ")
                        new_mileage = get_safe_int("New Mileage: ")
                        if sys.update_car_mileage(car_id, new_mileage):
                            print("Update successful.")
                        else:
                            print("Car not found.")

                    elif cmd == "4":  #Remove Car
                        car_id = get_safe_int("Car ID to remove: ")
                        if sys.remove_car(car_id):
                            print("Car removed.")
                        else:
                            print("Car not found.")

                    elif cmd == "5":  #Manage Bookings (WITH RISK SCORE DISPLAY)
                        pending = [b for b in sys.bookings if b.status == "Pending"]
                        if not pending:
                            print("\n--- No pending bookings found ---")
                        else:
                            print("\n--- Pending Bookings ---")
                            for b in pending:
                                score = sys.get_user_risk_score(b.user)
                                level = sys.risk_level(score)
                                print(f"ID:{b.b_id} | {b.user} | {b.car_info} | "
                                      f"Days:{b.days} | Total:${b.total_fee} | Risk:{level} ({score})")

                            bid = get_safe_int("ID to update (0 to cancel): ")
                            if bid != 0:
                                action = input("Approve (A) or Reject (R): ").upper().strip()
                                if action not in ["A", "R"]:
                                    print("!!! Invalid input. Use A or R.")
                                else:
                                    status = "Approved" if action == "A" else "Rejected"
                                    if sys.update_booking_status(bid, status):
                                        print(f"!!! Booking {bid} has been {status} successfully !!!")
                                    else:
                                        print("ID not found.")

                    elif cmd == "6":  #Logout
                        user = None
                        print("Logged out.")
                    else:
                        print("!!! Invalid admin option.")


                #CUSTOMER MENU

                elif user.role == "Customer":

                    if cmd == "1":  #View available cars
                        available_cars = [c for c in sys.cars if c.is_available]
                        if not available_cars:
                            print("\n--- No available cars at the moment ---")
                        else:
                            print("\n--- Available Cars ---")
                            for c in available_cars:
                                print(f"[{c.car_id}] {c.make} {c.model} - ${c.daily_rate}/day "
                                      f"(Min:{c.min_days} Max:{c.max_days})")

                    elif cmd == "2":  #Book a car (WITH PRICE BREAKDOWN + RECOMMENDATIONS)
                        car_id = get_safe_int("Car ID: ")
                        days = get_safe_int("Days: ")

                        result = sys.book_car(user, car_id, days)
                        print(result)

                        #Smart Recommendations ONLY when booking fails
                        if result.startswith("!!! Error"):
                            chosen = next((c for c in sys.cars if c.car_id == car_id), None)
                            target_rate = chosen.daily_rate if chosen else 60  # fallback rate
                            recs = sys.recommend_cars(target_rate=target_rate, limit=6)

                            #Filter out the selected car AND cars that don't support the requested days
                            filtered = [
                                c for c in recs
                                if c.car_id != car_id and (c.min_days <= days <= c.max_days)
                            ]

                            if filtered:
                                print("\n--- Recommended Alternatives (Closest Price) ---")
                                for c in filtered[:3]:  #keep it to top 3 results
                                    print(f"[{c.car_id}] {c.make} {c.model} - ${c.daily_rate}/day "
                                          f"(Min:{c.min_days} Max:{c.max_days})")
                            else:
                                print("\n--- No suitable alternative cars found for that rental period ---")


                    elif cmd == "3":  #View my booking status/history
                        mine = [b for b in sys.bookings if b.user == user.get_username()]
                        if not mine:
                            print("\n--- You have no booking history ---")
                        else:
                            print("\n--- My Bookings ---")
                            for b in mine:
                                print(f"ID {b.b_id}: {b.car_info} | Days:{b.days} | "
                                      f"Total:${b.total_fee} | Status: {b.status}")

                    elif cmd == "4":  #Logout
                        user = None
                        print("Logged out.")
                    else:
                        print("!!! Invalid customer option.")

        except Exception as e:
            #Global protection: prevents the system from crashing due to unexpected issues
            print(f"System Error: {e}")


if __name__ == "__main__":
    main()
