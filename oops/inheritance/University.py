class College:
    def __init__(self, college_name, location):
        self.college_name = college_name
        self.location = location

    def get_college_details(self):
        return f"College: {self.college_name}, Location: {self.location}"

class Department(College):  # Inherits from College
    def __init__(self, college_name, location, dept_name, hod):
        super().__init__(college_name, location)
        self.dept_name = dept_name
        self.hod = hod

    def get_department_details(self):
        return f"{self.get_college_details()}, Department: {self.dept_name}, HOD: {self.hod}"

class Student(Department):  # Inherits from Department
    def __init__(self, college_name, location, dept_name, hod, student_name, student_id):
        super().__init__(college_name, location, dept_name, hod)
        self.student_name = student_name
        self.student_id = student_id

    def get_student_details(self):
        return f"{self.get_department_details()}, Student: {self.student_name}, ID: {self.student_id}"

s = Student("ABC Engineering College", "Chennai", "EEE", "Dr. Aravind", "Jeeva", 12345)

print(s.get_student_details())
