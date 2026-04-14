import csv
import uuid
from datetime import date, datetime, timedelta



#ENSURE FILE EXISTS WITH HEADERS

def ensure_file(file_name, headers):
    try:
        with open(file_name, 'r'):
            pass
    except:
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)



# ADD PLANT        DONE BY: ABDULLA

def add_plant():
    ensure_file('plants.csv', ['id', 'name', 'location', 'date_acquired',
                              'watering_frequency', 'sunlight', 'last_watered'])
    ensure_file('growth.csv', ['plant_id', 'height', 'date'])
    ensure_file('photos.csv', ['plant_id', 'photo_path', 'date'])

    print("\n=== Add a New Plant ===")

    plant_id = str(uuid.uuid4())[:8]
    name = input("Enter plant name: ")
    location = input("Enter plant location: ")

    # Date
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

    # Watering
    while True:
        try:
            frequency = int(input("Enter watering frequency (times per day): "))
            if frequency > 0:
                break
            print("Enter a positive number.")
        except ValueError:
            print("Invalid input.")

    # Sunlight
    valid_sunlight = ['low', 'medium', 'high']
    while True:
        sunlight = input("Sunlight (Low/Medium/High): ").lower()
        if sunlight in valid_sunlight:
            break
        print("Enter Low, Medium, or High.")

    # Initial height
    while True:
        try:
            height = float(input("Enter initial height (cm): "))
            if height > 0:
                break
            print("Enter positive value.")
        except ValueError:
            print("Invalid input.")

    # Initial photo
    photo_path = input("Enter initial photo path: ")
    today = date.today().strftime("%Y-%m-%d")

    # Save plant
    new_plant = {
        'id': plant_id,
        'name': name,
        'location': location,
        'date_acquired': date_acquired,
        'watering_frequency': frequency,
        'sunlight': sunlight,
        'last_watered': ""
    }

    with open('plants.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=new_plant.keys())
        writer.writerow(new_plant)

    # Save growth
    with open('growth.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([plant_id, height, today])

    # Save photo
    with open('photos.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([plant_id, photo_path, today])

    print(f"\nPlant '{name}' added successfully!")



# RECORD CARE        DONE BY: YASSER


def record_care():
    ensure_file('care_log.csv', ['plant_id', 'activity', 'date'])

    print("\n=== Record Care Activity ===")

    plant_id = input("Enter plant ID: ")
    activity = input("Activity (Watering/Fertilizing/Repotting): ")
    today = date.today().strftime("%Y-%m-%d")

    with open('care_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([plant_id, activity, today])

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



# RECORD GROWTH        DONE BY: YASSER


def record_growth():
    ensure_file('growth.csv', ['plant_id', 'height', 'date'])

    print("\n=== Record Plant Growth ===")

    plant_id = input("Enter plant ID: ")

    while True:
        try:
            height = float(input("Enter height (cm): "))
            if height > 0:
                break
            print("Enter positive value.")
        except ValueError:
            print("Invalid input.")

    today = date.today().strftime("%Y-%m-%d")

    with open('growth.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([plant_id, height, today])

    print("Growth recorded!")



# ADD PHOTO        DONE BY: YASSER


def add_photo():
    ensure_file('photos.csv', ['plant_id', 'photo_path', 'date'])

    print("\n=== Add Plant Photo ===")

    plant_id = input("Enter plant ID: ")
    photo_path = input("Enter photo file path: ")
    today = date.today().strftime("%Y-%m-%d")

    with open('photos.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([plant_id, photo_path, today])

    print("Photo added!")




def get_latest_height(plant_id):
    try:
        with open('growth.csv', 'r') as file:
            reader = csv.DictReader(file)
            records = [r for r in reader if r.get('plant_id') == plant_id]
            if records:
                return records[-1].get('height', "N/A")
    except:
        pass
    return "N/A"


def get_latest_photo(self_id):
    try:
        with open('photos.csv', 'r') as file:
            reader = csv.DictReader(file)
            records = [r for r in reader if r.get('plant_id') == self_id]
            if records:
                return records[-1].get('photo_path', "N/A")
    except:
        pass
    return "N/A"



# VIEW ALL        DONE BY: MAHMOOD


def view_all_plants():
    print("\n=== All Plants ===")

    try:
        with open('plants.csv', 'r') as file:
            reader = csv.DictReader(file)

            for plant in reader:
                height = get_latest_height(plant['id'])
                photo = get_latest_photo(plant['id'])

                print(f"""
ID: {plant['id']}
Name: {plant['name']}
Location: {plant['location']}
Watering Frequency: {plant['watering_frequency']} days
Sunlight: {plant['sunlight']}
Last Watered: {plant['last_watered']}
Latest Height: {height} cm
Latest Photo: {photo}
---------------------------
""")
    except:
        print("No plants found.")



# VIEW DUE        DONE BY: MAHMOOD

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



# SEARCH        DONE BY: MAHMOOD

def search_plants():
    print("\n=== Search Plants ===")
    term = input("Enter name or location: ").lower()

    with open('plants.csv', 'r') as file:
        reader = csv.DictReader(file)

        for plant in reader:
            if term in plant['name'].lower() or term in plant['location'].lower():
                print(plant)



# MENU        DONE BY: MAHMOOD

def display_menu():
    print("\n=== Plant Care Tracker ===")
    print("1. Add a new plant")
    print("2. Record care activity")
    print("3. View plants due for care")
    print("4. Search plants")
    print("5. View all plants")
    print("6. Record plant growth")
    print("7. Add plant photo")
    print("8. Exit")
    return input("Enter your choice: ")



# MAIN        DONE BY: MAHMOOD

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
            record_growth()
        elif choice == '7':
            add_photo()
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
