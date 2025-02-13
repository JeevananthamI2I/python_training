class College:  # Base Class
    def __init__(self, college_name, location):
        self.college_name = college_name
        self.location = location

    def get_college_details(self):
        return f"College: {self.college_name}, Location: {self.location}"

class Department(College):  # Child Class 1
    def __init__(self, college_name, location, dept_name):
        super().__init__(college_name, location)
        self.dept_name = dept_name

    def get_department_details(self):
        return f"{self.get_college_details()}, Department: {self.dept_name}"

class Student(College):  # Child Class 2
    def __init__(self, college_name, location, student_name, student_id):
        super().__init__(college_name, location)
        self.student_name = student_name
        self.student_id = student_id

    def get_student_details(self):
        return f"{self.get_college_details()}, Student: {self.student_name}, ID: {self.student_id}"

dept = Department("ABC University", "Chennai", "EEE")
student = Student("ABC University", "Chennai", "Jeeva", 100)

print(dept.get_department_details())

print(student.get_student_details())
