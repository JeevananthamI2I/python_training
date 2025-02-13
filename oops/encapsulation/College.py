class College:
    def __init__(self, name, code, location):
        self.__college_name = name          
        self.__college_code = code          
        self.__college_location = location 

    # Getter methods
    def get_college_name(self):
        return self.__college_name

    def get_college_code(self):
        return self.__college_code

    def get_college_location(self):
        return self.__college_location

    # Setter methods
    def set_college_name(self, name):
        self.__college_name = name

    def set_college_code(self, code):
        self.__college_code = code

    def set_college_location(self, location):
        self.__college_location = location

    def display_details(self):
        print(f"College Name: {self.__college_name}")
        print(f"College Code: {self.__college_code}")
        print(f"College Location: {self.__college_location}")

college = College("XYZ University", "AB123", "Chennai")

print("Before Modification:")
college.display_details()

college.set_college_name("XYZ University")
college.set_college_code("ABCD01")
college.set_college_location("chennai, Tamilnadu")

print("\nAfter Modification:")
college.display_details()

