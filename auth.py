import bcrypt
import os
import string

USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    # Encode both the plaintext password and stored hash to bytes
     password_bytes = plain_text_password.encode('utf-8')
     hashed_password_bytes = hashed_password.encode('utf-8')
    # bcrypt.checkpw handles extracting the salt and comparing
     return bcrypt.checkpw(password_bytes, hashed_password_bytes)

test_password = "SecurePassword123"
# Test hashing
hashed = hash_password(test_password)
print(f"Original password: {test_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")
# Test verification with correct password
is_valid = verify_password(test_password, hashed)
print(f"\nVerification with correct password: {is_valid}")
# Test verification with incorrect password
is_invalid = verify_password("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")

def register_user(username, password):
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                stored_username, _ = line.strip().split(",", 1)
                if stored_username == username:
                    return False
    hashed_password = hash_password(password)
    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")
    print(f"User '{username}' registered.")
    return True

def user_exists(username):
    if not os.path.exists("user.txt"):
        return False
    with open("users.txt", "r") as f:
        for line in f:
            stored_username, _ = line.strip().split(",", 1)
            if stored_username == username:
                return True
    return False

def login_user(username, password):
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt", "r") as f:
        for line in f:
            user, stored_hash = line.strip().split(",", 1)
    if user == username:
        return verify_password(password< stored_hash)
    return False

def validate_username(username):
    username = ("Enter username:")
    if len(username) < 3:
        return False
    print("Username must be at least 3 characters long.")
    if username.isalnum() == False:
        print("username can only contains numbers and letters.")
        return False
    print("Username is valid.")

def validate_password(password):
    password = ("Enter password: ")
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
    else:
        print("password is valid")
        return
    has_letter == False
    for c in password:
        has_letter = True
        break
    if has_letter == False:
        print("Password must contain at  least one letter ")
        return
        has_digit = False
        for c in password:
            if c.isdigit():
                has_digit = True
                break
        if has_digit == False:
            print("Password must contain at least one number.")
            return
        print("Password is valid!")

def main():
   print("\nWelcome to the Week 7 Authentication System!")

   while True:
      display_menu()
      choice = input("\nPlease select an option (1-3): ").strip()
      if choice == '1':                   #Registration flow
           print("\n--- USER REGISTRATION ---")
           username = input("Enter a username: ").strip()

      # Validate username
           is_valid, error_msg = validate_username(username)
           if not is_valid:
               print(f"Error: {error_msg}")
               continue
           password = input("Enter a password: ").strip()
           # Validate password
           is_valid, error_msg = validate_password(password)
           if not is_valid:
              print(f"Error: {error_msg}")
              continue

              password_confirm = input("Confirm password: ").strip()
              if password != password_confirm:
                  print("Error: Passwords do not match.")
                  continue

                  # Register the user
                  register_user(username, password)
              elif choice == '2':
                  print("\n--- USER LOGIN ---")
                  username = input("Enter your username: ").strip()
                  password = input("Enter your password: ").strip()
                  if login_user(username, password):
                      print("\nYou are now logged in.")
                      input("\nPress Enter to return to main menu...")      #Ask if user wants to logout
              elif choice == '3':
                  print("\nThank you for using the authentication system.")
                  print("Exiting...")
                  break
              else:
                  print("\nError: Invalid option. Please select 1, 2, or 3.")
                  if _name_ == "_main_":
                      main()
                      