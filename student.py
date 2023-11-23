import streamlit as st

# Base Class: Student
class Student:
    def __init__(self, name, age, grade, address, contact_number, marks):
        self._name = name
        self._age = age
        self._grade = grade
        self._address = address
        self._contact_number = contact_number
        self._marks = marks

    def calculate_grade(self):
        if self._marks > 90:
            return "A"
        elif self._marks >= 80:
            return "B"
        elif self._marks >= 70:
            return "C"
        else:
            return "D"

    def display_details(self):
        details = {
            "Name": self._name,
            "Age": self._age,
            "Grade": self._grade,
            "Address": self._address,
            "Contact Number": self._contact_number,
            "Marks": self._marks,
            "Grade": self.calculate_grade()
        }
        return details


# Derived Class: StudentMarks (Inherits from Student)
class StudentMarks(Student):
    def __init__(self, name, age, grade, address, contact_number, marks, subjects):
        super().__init__(name, age, grade, address, contact_number, marks)
        self._subjects = subjects

    def display_details(self):
        details = super().display_details()
        details["Subjects"] = self._subjects
        return details


# Streamlit UI
def main():
    st.title("Student Details and Marks")

    # User input for common student details
    name = st.text_input("Enter Student Name:")
    age = st.number_input("Enter Student Age:")
    grade = st.text_input("Enter Student Grade:")
    address = st.text_area("Enter Address:")
    contact_number = st.text_input("Enter Contact Number:")
    marks = st.number_input("Enter Overall Marks:")

    # User input for subjects and grades
    st.write("Enter Subjects and Grades:")
    subjects = {}
    while True:
        subject = st.text_input("Subject:")
        if not subject:
            break
        grade = st.text_input(f"Grade in {subject}:")
        subjects[subject] = grade

    # Create an instance of StudentMarks
    student = StudentMarks(name, age, grade, address, contact_number, marks, subjects)

    # Display student details and marks in a table
    details = student.display_details()
    st.table([details])


if __name__ == "__main__":
    main()

