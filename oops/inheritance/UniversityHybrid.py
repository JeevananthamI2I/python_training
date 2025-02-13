class College:  # Base Class
    def __init__(self, college_name, location):
        self.college_name = college_name
        self.location = location

    def get_college_details(self):
        return f"College: {self.college_name}, Location: {self.location}"

class Department(College):
    def __init__(self, college_name, location, dept_name):
        super().__init__(college_name, location)
        self.dept_name = dept_name

    def get_department_details(self):
        return f"{self.get_college_details()}, Department: {self.dept_name}"

class Sports:
    def __init__(self, sport_name):
        self.sport_name = sport_name

    def get_sport_details(self):
        return f"Sport: {self.sport_name}"

class Student(Department, Sports):
    def __init__(self, college_name, location, dept_name, student_name, student_id, sport_name):
        Department.__init__(self, college_name, location, dept_name) 
        Sports.__init__(self, sport_name)  
        self.student_name = student_name
        self.student_id = student_id

    def get_student_details(self):
        return f"{self.get_department_details()}, Student: {self.student_name}, ID: {self.student_id}, {self.get_sport_details()}"

s = Student("ABC Engineering College", "Chennai", "EEE", "Dr. Aravind", "Jeeva", "cricket")

print(s.get_student_details())
