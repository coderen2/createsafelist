import os
import json
import bcrypt
import getpass
import subprocess

# Initialize global variables
file_name = "data.json"
data = {
    "account": {
        "username": None,
        "password_hash": None
    },
    "favorites": {}
}

def save_data():
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    global data
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            data = json.load(file)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def check_bcrypt_installed():
    try:
        subprocess.check_call(["pip", "show", "bcrypt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def show_more_options():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("More Options")
        print("=" * 30)
        print("1. Nederlands")
        print("2. English (USA)")
        print("3. 日本語 (Japanese)")
        print("4. Français (French)")

        choice = input("Choose a language: ")
        if choice == "1":
            message = "Voordat je gaat opslaan is het best om deze stappen te volgen:\n1. Druk op Win + R\n2. Typ cmd\n3. Voer in: pip install bcrypt"
        elif choice == "2":
            message = "Before you save, it is best to follow these steps:\n1. Press Win + R\n2. Type cmd\n3. Enter: pip install bcrypt"
        elif choice == "3":
            message = "保存する前に、次の手順を実行することをお勧めします:\n1. Win + Rを押す\n2. cmdと入力する\n3. 次を入力: pip install bcrypt"
        elif choice == "4":
            message = "Avant de sauvegarder, il est préférable de suivre ces étapes:\n1. Appuyez sur Win + R\n2. Tapez cmd\n3. Saisissez: pip install bcrypt"
        else:
            print("Invalid choice. Try again.")
            input("Press Enter to continue...")
            continue

        print("=" * 30)
        print(message)

        if check_bcrypt_installed():
            print("\nBcrypt is already installed on your system!")
        else:
            print("\nBcrypt is NOT installed. Please install it before proceeding.")

        input("\nPress Enter to return to the main menu...")
        break

def ensure_bcrypt_installed():
    while not check_bcrypt_installed():
        show_more_options()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Checking for bcrypt again...")
        if not check_bcrypt_installed():
            print("bcrypt is still not installed. Returning to instructions.")
            input("Press Enter to continue...")
        else:
            print("bcrypt successfully detected. Proceeding...")
            break

def create_account():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Create Account")
        print("="*30)
        username = input("Username: ")
        password = getpass.getpass("Create Password: ")
        redo_password = getpass.getpass("Redo Password: ")

        if password != redo_password:
            print("Passwords do not match. Try again.")
            input("Press Enter to continue...")
            continue

        data["account"]["username"] = username
        data["account"]["password_hash"] = hash_password(password)
        save_data()

        print("Account created successfully!")
        print("Warning: If you forget your password, you'll lose all saved data.")
        input("Press Enter to continue...")
        break

def login():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Login")
        print("="*30)
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        if username == data["account"]["username"] and verify_password(password, data["account"]["password_hash"]):
            print("Login successful!")
            input("Press Enter to continue...")
            return True
        else:
            print("Invalid username or password. Try again.")
            input("Press Enter to continue...")

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Main Menu")
        print("="*30)
        print("1. Add")
        print("2. Remove")
        print("3. View Sites")
        print("4. Save to .json")
        print("5. More Options")
        print("6. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            add_menu()
        elif choice == "2":
            remove_menu()
        elif choice == "3":
            view_sites()
        elif choice == "4":
            save_data()
            print("Data saved successfully!")
            input("Press Enter to continue...")
        elif choice == "5":
            show_more_options()
        elif choice == "6":
            print("Exiting...")
            if input("Do you want to save changes? (y/n): ").lower() == "y":
                save_data()
            break
        else:
            print("Invalid choice. Try again.")
            input("Press Enter to continue...")

def add_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Add Menu")
    print("="*30)
    print("1. Add Favorite Site Group")
    print("2. Add Site to Group")

    choice = input("Choose an option: ")
    if choice == "1":
        group_name = input("Enter the name of the new favorite site group: ")
        if group_name in data["favorites"]:
            print("Group already exists!")
        else:
            data["favorites"][group_name] = []
            print(f"Group '{group_name}' added successfully!")
            print("="*30)
            print(f"[ {group_name} ] is now active.")
            print("="*30)
    elif choice == "2":
        if not data["favorites"]:
            print("No groups available. Add a group first.")
        else:
            print("Available Groups:")
            for i, group in enumerate(data["favorites"].keys(), 1):
                print(f"{i}. {group}")
            group_choice = int(input("Select a group by number: ")) - 1
            group_name = list(data["favorites"].keys())[group_choice]
            site = input(f"Enter site to add to '{group_name}': ")
            email_or_username = input("Enter email/username (or leave blank if none): ")
            password = getpass.getpass("Enter password (or leave blank if none): ")

            site_entry = {
                "url": site,
                "email_or_username": email_or_username if email_or_username else None,
                "password": hash_password(password) if password else None
            }

            data["favorites"][group_name].append(site_entry)
            print(f"Site added to '{group_name}'!")
    else:
        print("Invalid choice. Returning to main menu.")
    input("Press Enter to continue...")

def remove_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Remove Menu")
    print("="*30)
    print("1. Remove Favorite Site Group")
    print("2. Remove Site from Group")

    choice = input("Choose an option: ")
    if choice == "1":
        if not data["favorites"]:
            print("No groups available to remove.")
        else:
            print("Available Groups:")
            for i, group in enumerate(data["favorites"].keys(), 1):
                print(f"{i}. {group}")
            group_choice = int(input("Select a group to remove by number: ")) - 1
            group_name = list(data["favorites"].keys())[group_choice]

            confirm = input(f"Are you sure you want to delete '{group_name}'? (y/n): ").lower()
            if confirm == "y":
                data["favorites"].pop(group_name)
                print(f"Group '{group_name}' deleted!")
    elif choice == "2":
        if not data["favorites"]:
            print("No groups available to remove sites from.")
        else:
            print("Available Groups:")
            for i, group in enumerate(data["favorites"].keys(), 1):
                print(f"{i}. {group}")
            group_choice = int(input("Select a group by number: ")) - 1
            group_name = list(data["favorites"].keys())[group_choice]

            if not data["favorites"][group_name]:
                print(f"No sites in group '{group_name}'.")
            else:
                print("Available Sites:")
                for i, site in enumerate(data["favorites"][group_name], 1):
                    print(f"{i}. {site['url']}")
                site_choice = int(input("Select a site to remove by number: ")) - 1
                site = data["favorites"][group_name].pop(site_choice)
                print(f"Site '{site['url']}' removed from '{group_name}'.")
    else:
        print("Invalid choice. Returning to main menu.")
    input("Press Enter to continue...")

def view_sites():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("View Sites")
    print("="*30)
    if not data["favorites"]:
        print("No favorite sites available.")
    else:
        for group, sites in data["favorites"].items():
            print("="*30)
            print(f"[ {group} ]")
            print("="*30)
            if sites:
                for site in sites:
                    print(f"  - URL: {site['url']}")
                    if site['email_or_username']:
                        print(f"    Email/Username: {site['email_or_username']}")
                    if site['password']:
                        print(f"    Password: {'*' * 8} (hidden)")
            else:
                print("  (No sites)")
    input("Press Enter to continue...")

# Main program execution
if __name__ == "__main__":
    load_data()

    # Ensure bcrypt is installed
    ensure_bcrypt_installed()

    if data["account"]["username"] is None:
        create_account()

    if login():
        main_menu()