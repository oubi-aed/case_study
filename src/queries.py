import os
from tinydb import TinyDB, Query
from serializer import serializer

def find_devices() -> list:
    """Find all devices in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')
    # Search the database for all devices that are active
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [x["device_name"] for x in result]
    
    return result

def store_user_data(user_name: str, user_email: str, user_role: str):
    """Store user data in the database."""
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('users')
    user_data = {
        "user_name": user_name,
        "user_email": user_email,
        "user_role": user_role
    }
    db_connector.insert(user_data)

if __name__ == "__main__":
    print(find_devices())