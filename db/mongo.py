from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import List, Dict, Union, Optional
from settings import MONGO_URI


# Establish a connection with the MongoDB database
client = MongoClient(MONGO_URI)
db = client['velib_db']
users_collection = db['users']


def add_user(email: str, is_premium: bool = False) -> Union[str, None]:
    """
    Add a new user to the database.

    Args:
        email (str): User's email address
        is_premium (bool): Whether the user has a premium subscription. Defaults to False.

    Returns:
        str or None: Returns an error message if the operation fails, None otherwise.
    """
    user = {
        "email": email,
        "is_premium": is_premium,
        "preferences": []
    }
    try:
        users_collection.insert_one(user)
    except PyMongoError as e:
        return str(e)


def add_or_update_preference(email: str, station_name: str, time_slot: str) -> Union[str, None]:
    """
    Add or update a user's station preference.

    Args:
        email (str): User's email address
        station_name (str): Name of the station
        time_slot (str): Preferred time slot for notifications

    Returns:
        str or None: Returns an error message if the operation fails, None otherwise.
    """
    user = get_user_by_email(email)
    if not user:
        return "User not found"

    # Check if station preference already exists
    pref_exists = next((p for p in user["preferences"] if p["station"] == station_name), None)

    try:
        if pref_exists:
            # Update the existing preference's notification time
            users_collection.update_one({"email": email, "preferences.station": station_name},
                                        {"$set": {"preferences.$.notification_time": time_slot}})
        else:
            # Add a new preference
            new_pref = {"station": station_name, "notification_time": time_slot}
            users_collection.update_one({"email": email}, {"$push": {"preferences": new_pref}})
    except PyMongoError as exception:
        return str(exception)


def get_all_users() -> List[Dict]:
    """
    Fetch all users from the database.

    Returns:
        List[Dict]: A list of user documents.
    """
    try:
        return list(users_collection.find({}))
    except PyMongoError as exception:
        print(f"Exception: {exception}")
        return []


def get_user_by_email(email: str) -> Optional[Dict]:
    """
    Fetch a user by email from the database.

    Args:
        email (str): User's email address

    Returns:
        Dict or None: A user document if found, None otherwise.
    """
    try:
        return users_collection.find_one({"email": email})
    except PyMongoError as e:
        return None


def update_user(email: str, updated_data: Dict) -> Union[str, None]:
    """
    Update a user's information in the database.

    Args:
        email (str): User's email address
        updated_data (Dict): The data to update

    Returns:
        str or None: Returns an error message if the operation fails, None otherwise.
    """
    try:
        users_collection.update_one({"email": email}, {"$set": updated_data})
    except PyMongoError as e:
        return str(e)


def delete_user(email: str) -> Union[str, None]:
    """
    Delete a user from the database.

    Args:
        email (str): User's email address

    Returns:
        str or None: Returns an error message if the operation fails, None otherwise.
    """
    try:
        users_collection.delete_one({"email": email})
    except PyMongoError as e:
        return str(e)


def get_user_preferences(email: str) -> Union[List[Dict], None]:
    """
    Fetch a user's station preferences from the database.

    Args:
        email (str): User's email address

    Returns:
        List[Dict] or None: A list of user preferences if found, None otherwise.
    """
    user = get_user_by_email(email)
    if user:
        return user.get("preferences", [])
    return None
