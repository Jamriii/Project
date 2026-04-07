import csv
import uuid
from datetime import date, datetime, timedelta

# adding a new plant
def add_plant():
    """Add a new plant to plants.csv"""

    # Initialize file
    try:
        with open('plants.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
        print('\nplants.csv exists.')
    except:
        with open('plants.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'location', 'date_acquired',
                             'watering_frequency', 'sunlight', 'last_watered'])
        print('\nNew plants.csv created.')

    print("\n=== Add a New Plant ===")

    plant_id = str(uuid.uuid4())[:8]

    name = input("Enter plant name: ")
    location = input("Enter plant location: ")

    # Validate date
    while True:
        date_acquired = input("Enter date acquired (YYYY-MM-DD) or press Enter for today: ")
        if not date_acquired.strip():
            date_acquired = date.today().strftime("%Y-%m-%d")
            break
        try:
            datetime.strptime(date_acquired, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format.")

    # Validate watering frequency
    while True:
        try:
            frequency = int(input("Enter watering frequency (days): "))
            if frequency > 0:
                break
            print("Enter a positive number.")
        except ValueError:
            print("Invalid input.")

    # Validate sunlight
    valid_sunlight = ['low', 'medium', 'high']
    while True:
        sunlight = input("Sunlight (Low/Medium/High): ").lower()
        if sunlight in valid_sunlight:
            break
        print("Enter Low, Medium, or High.")

    new_plant = {
        'id': plant_id,
        'name': name,
        'location': location,
        'date_acquired': date_acquired,
        'watering_frequency': frequency,
        'sunlight': sunlight,
        'last_watered': ""
    }

    try:
        with open('plants.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=new_plant.keys())
            writer.writerow(new_plant)
        print(f"\nPlant '{name}' added successfully!")
    except Exception as e:
        print(f"Error saving plant: {e}")


# =========================
# RECORD CARE ACTIVITY
# =========================
def record_care():
    """Record plant care activity"""

    # Ensure log file exists
    try:
        with open('care_log.csv', 'r'):
            print('\ncare_log.csv exists.')
    except:
        with open('care_log.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['plant_id', 'activity', 'date'])
        print('\nNew care_log.csv created.')

    print("\n=== Record Care Activity ===")

    plant_id = input("Enter plant ID: ")
    activity = input("Activity (Watering/Fertilizing/Repotting/Pruning): ")
    today = date.today().strftime("%Y-%m-%d")

    with open('care_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([plant_id, activity, today])

    # Update last watered
    if activity.lower() == "watering":
        update_last_watered(plant_id, today)

    print("Care activity recorded!")


def update_last_watered(plant_id, today):
    rows = []

    with open('plants.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == plant_id:
                row['last_watered'] = today
            rows.append(row)

    with open('plants.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


# =========================
# VIEW PLANTS DUE FOR CARE
# =========================
def view_due_plants():
    print("\n=== Plants Due for Watering ===")

    today = datetime.today()

    with open('plants.csv', 'r') as file:
        reader = csv.DictReader(file)

        for plant in reader:
            if plant['last_watered']:
                last = datetime.strptime(plant['last_watered'], "%Y-%m-%d")
                freq = int(plant['watering_frequency'])

                if today >= last + timedelta(days=freq):
                    print(f"{plant['name']} ({plant['location']})")


# =========================
# SEARCH PLANTS
# =========================
def search_plants():
    print("\n=== Search Plants ===")
    term = input("Enter name or location: ").lower()

    with open('plants.csv', 'r') as file:
        reader = csv.DictReader(file)

        for plant in reader:
            if term in plant['name'].lower() or term in plant['location'].lower():
                print(plant)


# =========================
# VIEW ALL PLANTS
# =========================
def view_all_plants():
    print("\n=== All Plants ===")

    try:
        with open('plants.csv', 'r') as file:
            reader = csv.DictReader(file)
            for plant in reader:
                print(plant)
    except:
        print("No plants found.")


# =========================
# MENU
# =========================
def display_menu():
    print("\n=== Plant Care Tracker ===")
    print("1. Add a new plant")
    print("2. Record care activity")
    print("3. View plants due for care")
    print("4. Search plants")
    print("5. View all plants")
    print("6. Exit")
    return input("Enter your choice: ")


# =========================
# MAIN LOOP
# =========================
def main():
    print("Welcome to Plant Care Tracker!")

    while True:
        choice = display_menu()

        if choice == '1':
            add_plant()
        elif choice == '2':
            record_care()
        elif choice == '3':
            view_due_plants()
        elif choice == '4':
            search_plants()
        elif choice == '5':
            view_all_plants()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()