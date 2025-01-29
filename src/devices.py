import os
from datetime import datetime, date
from tinydb import TinyDB, Query
from serializer import serializer


class Device():
    # Class variable that is shared between all instances of the class
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')

    # Constructor
    def __init__(self, device_name: str, managed_by_user_id: str, last_maintenance_date: str, maintenance_cost: str, maintenance_frequency: str, reserved_by: str = "", reservations=None):
        self.device_name = device_name
        self.managed_by_user_id = managed_by_user_id
        self.is_active = True
        self.last_maintenance_date = last_maintenance_date or ""
        self.maintenance_cost = maintenance_cost or ""
        self.maintenance_frequency = maintenance_frequency or ""
        self.reserved_by = reserved_by
        self.reservations = reservations if reservations is not None else []

    def add_reservation(self, reserved_by, start_date, end_date):
        reservation = {
            "reserved_by": reserved_by,
            "start_date": start_date,
            "end_date": end_date
        }
        self.reservations.append(reservation)

    def is_reserved(self, start_date, end_date):
        for reservation in self.reservations:
            if (start_date <= reservation['end_date'] and end_date >= reservation['start_date']):
                return True
        return False

    def store_data(self):
        print("Storing data...")
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        if result:
            self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1):
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery[by_attribute] == attribute_value)
        if result:
            data = result[:num_to_return]
            device_results = [cls(d['device_name'], d['managed_by_user_id'], d.get('last_maintenance_date', ""), d.get('maintenance_cost', ""), d.get('maintenance_frequency', ""), d.get('reserved_by', ""), d.get('reservations', [])) for d in data]
            return device_results if num_to_return > 1 else device_results[0]
        else:
            return None

    @classmethod
    def find_all(cls) -> list:
        devices = []
        for device_data in Device.db_connector.all():
            devices.append(Device(device_data['device_name'], device_data['managed_by_user_id'], device_data.get('last_maintenance_date', ""), device_data.get('maintenance_cost', ""), device_data.get('maintenance_frequency', ""), device_data.get('reserved_by', ""), device_data.get('reservations', [])))
        return devices


if __name__ == "__main__":
    device1 = Device("Device1", "one@mci.edu", "", "", "")
    device1.store_data()
    loaded_device = Device.find_by_attribute("device_name", "Device1")
    if loaded_device:
        print(f"Loaded Device: {loaded_device}")
    else:
        print("Device not found.")
    devices = Device.find_all()
    print("All devices:")
    for device in devices:
        print(device)