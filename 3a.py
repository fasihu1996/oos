import requests
from bs4 import BeautifulSoup

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

    @classmethod
    def get_no_of_students(cls):
        return Student.number_of_students

    def __str__(self):
        return f"Student id: {self.id_number}\nLast name: {self.lastname}\nFirst name: {self.firstname}\n"

fasih = Student("Uddin", "Fasih", 12345)
print(fasih)
print(Student.get_no_of_students())


def get_urls(url):
    r  = requests.get(url)
    #print(r.text)
    soup = BeautifulSoup(r.content, 'html.parser')
    website_urls = []
    for link in soup('a', href=True):
        href = link['href']
        keywords = link.get_text().split()
        website_urls.append((href, keywords))

    return website_urls, len(website_urls)

def print_urls(urls_with_keywords):
    for url, keywords in urls_with_keywords:
        print(f"URL: {url}")
        print(f"Keywords: {', '.join(keywords)}")
        print("-" * 40)

urls, count = get_urls('https://th-brandenburg.de')
#print_urls(urls)
#print(f"Total URLs found: {count}")
#print(get_urls('https://th-brandenburg.de'))


