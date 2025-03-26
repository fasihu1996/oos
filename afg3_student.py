class Student:

    number_of_students = 0
    def __init__(self, lastname, firstname, id_number):
        self.lastname = lastname
        self.firstname = firstname
        self.id_number = id_number
        self.courses = []
        Student.number_of_students += 1

    def get_details(self):
        return self.lastname, self.firstname, self.id_number

    def enroll(self, course):
        if course not in self.courses:
            self.courses.append(course)
        else:
            return "The student is already enrolled in that course."

    def get_courses(self):
        return self.courses

    @classmethod
    def get_no_of_students(cls):
        return Student.number_of_students

    def __str__(self):
        return f"Student id: {self.id_number}\nLast name: {self.lastname}\nFirst name: {self.firstname}\n"

if __name__ == '__main__':
    fasih = Student("Uddin", "Fasih", 12345)
    print(fasih)
    print(Student.get_no_of_students())





