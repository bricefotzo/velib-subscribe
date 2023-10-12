import sys
from utils.helpers import notify_user

def main():
    """
    Main function to notify the user about the bike station status.
    """
    try:
        # Fetch command line arguments
        email = sys.argv[1]
        station = sys.argv[2]

        # Notify the user
        notify_user(email, station)
        
    except IndexError:
        print("Error: Missing command line arguments. Usage: python <script_name> <email> <station>")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
