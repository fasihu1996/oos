import requests, unittest
from afg3_student import Student

class TestStudent(unittest.TestCase):

    def test_student_creation(self):
        actual = Student("Uddin", "Fasih", 1234)
        self.assertEqual(actual.__str__(), f"Student id: {actual.id_number}\nLast name: {actual.lastname}\nFirst name: {actual.firstname}\n")
        self.assertEqual(actual.get_no_of_students(), 1)

    def testenrollment(self):
        actual = Student("Uddin", "Fasih", 1234)
        actual.enroll("OOSL")
        self.assertEqual(actual.get_courses(), actual.courses)
        self.assertEqual(actual.get_no_of_students(), 2)


if __name__ == '__main__':
    unittest.main()


