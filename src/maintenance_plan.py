class MaintenancePlan:
    def __init__(self, first_maintenance, next_maintenance, __maintenance_interval: int, __maintenance_cost: float) -> None:
        """Create a maintenance Plan"""
        self.first_maintenance = first_maintenance
        self.next_maintenance = next_maintenance
        self.__maintenance_interval = __maintenance_interval
        self.__maintenance_cost = __maintenance_cost

    def store_data(self)-> None:
        """Save the maintenance plan to the database"""
        pass

    def delete(self) -> None:
        """Delete the maintenance plan"""
        pass
    
    def __str__(self):
        return f"maintenance_plan {self.first_maintenance} - {self.next_maintenance} - {self.__maintenance_interval} - {self.__maintenance_cost}"
    
    def __repr__(self):
        return self.__str__()
    
    def maintenance_cost_per_quarter(self) -> float:
        """Calculate the maintenance cost per quarter"""
        pass
    """
    @staticmethod
    def find_all(cls) -> list:
        Find all users in the database
        pass

    @classmethod
    def find_by_attribute(cls, by_attribute : str, attribute_value : str) -> 'User':
        From the matches in the database, select the user with the given attribute value
        pass
        
        """