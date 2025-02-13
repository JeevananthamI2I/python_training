from abc import ABC, abstractmethod

class College(ABC):  
    def __init__(self, name, location):
        self.name = name
        self.location = location
    
    @abstractmethod
    def get_courses(self):
        pass

    @abstractmethod
    def get_fee_structure(self):
        pass

class PlacementCell(ABC):
    @abstractmethod
    def get_placement_stats(self):
        pass

class EngineeringCollege(College, PlacementCell):
    def get_courses(self):
        return ["Computer Science", "Mechanical", "Civil", "Electronics"]
    
    def get_fee_structure(self):
        return "Fees: 5000/- per semester"

    def get_placement_stats(self):
        return "Placement Rate: 95%, Highest Package: 100,000/-"


eng_college = EngineeringCollege("Tech Institute", "Chennai")

print(f"{eng_college.name} offers courses: {eng_college.get_courses()}")
print(f"{eng_college.name} - {eng_college.get_fee_structure()}")
print(f"{eng_college.name} - {eng_college.get_placement_stats()}")
