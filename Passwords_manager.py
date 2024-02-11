from cryptography.fernet import Fernet
import base64


def generate_key_if_needed():
    """Generates a new key if it doesn't exist, otherwise loads the existing key."""
    try:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
            if len(key) != 32:  # Check if existing key has correct length
                raise ValueError("Existing key is invalid. Generating new key.")
            return key
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key


def get_master_password():
    """Prompts the user for the master password."""
    master_pwd = input("What is the master password? ")
    return master_pwd.encode()


def create_fernet(master_pwd):
    """Creates a Fernet object using the combined key."""
    key = generate_key_if_needed()
    combined_key = key + master_pwd
    return Fernet(combined_key)


def view_passwords(fer):
    """Views the stored passwords."""
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            decrypted_password = fer.decrypt(passw.encode()).decode()
            print("Username:", user, "| Password:", decrypted_password)


def add_password(fer):
    """Adds a new password to the file."""
    username = input("Account name or User name: ")
    pwd = input("Password: ")
    encrypted_password = fer.encrypt(pwd.encode()).decode()
    with open('passwords.txt', 'a') as f:
        f.write(username + "|" + encrypted_password + '\n')


def main():
    """Main function to handle user interaction."""
    fer = create_fernet(get_master_password())
    while True:
        mode = input("Would you like to add a new password, view existing ones, or quit? (add/view/quit) ").lower()
        if mode == "quit":
            break
        elif mode == "view":
            view_passwords(fer)
        elif mode == "add":
            add_password(fer)
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
