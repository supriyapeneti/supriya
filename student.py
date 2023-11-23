import streamlit as st

class Student:
    def __init__(self, name, age, grade, address, contact_number, marks):
        self.name = name
        self.age = age
        self.grade = grade
        self.address = address
        self.contact_number = contact_number
        self.marks = marks

    def calculate_grade(self):
        if self.marks > 90:
            return "A"
        elif self.marks >= 80:
            return "B"
        elif self.marks >= 70:
            return "C"
        else:
            return "D"

# Streamlit UI
def main():
    st.title("Student Details and Marks")

    # Input details for multiple students
    students = []
    while st.button("Add Student"):
        st.write(f"\n--- Student {len(students) + 1} ---")
        # User input for common student details
        name = st.text_input("Enter Student Name:")
        age = st.number_input("Enter Student Age:")
        grade = st.text_input("Enter Student Grade:")
        address = st.text_area("Enter Address:")
        contact_number = st.text_input("Enter Contact Number:")
        marks = st.number_input("Enter Overall Marks:")

        # Create an instance of Student
        student = Student(name, age, grade, address, contact_number, marks)
        students.append(student)

    # Display student details and marks in a table
    details_list = []
    for i, student in enumerate(students, 1):
        details = {
            "Student": i,
            "Name": student.name,
            "Age": student.age,
            "Grade": student.grade,
            "Address": student.address,
            "Contact Number": student.contact_number,
            "Marks": student.marks,
            "Grade": student.calculate_grade()
        }
        details_list.append(details)

    st.table(details_list)

if __name__ == "__main__":
    main()
