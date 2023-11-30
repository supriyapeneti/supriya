import streamlit as st
import pandas as pd
import psycopg2

# Install openpyxl if not present
try:
    import openpyxl
except ImportError:
    st.warning("openpyxl not found. Please install it using: pip install openpyxl")
    import openpyxl  # Verify if the installation was successful

# Create a connection to the PostgreSQL database
conn = psycopg2.connect(
    database="employee1", user='user', password='5001', host='127.0.0.1', port='5432'
)
cursor = conn.cursor()

# Create a table to store employee information if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    assigned_tasks INTEGER NOT NULL,
    completed_tasks INTEGER NOT NULL,
    total_attendance INTEGER NOT NULL,
    total_leaves INTEGER NOT NULL,
    performance_percentage FLOAT
);
'''
cursor.execute(create_table_query)
conn.commit()

# Employee class
class Employee:
    def __init__(self, name, assigned_tasks, total_attendance, total_leaves, completed_tasks):
        self.name = name
        self.assigned_tasks = assigned_tasks
        self.completed_tasks = completed_tasks
        self.total_attendance = total_attendance
        self.total_leaves = total_leaves
        self.performance_percentage = None

    def calculate_performance(self):
        task_performance = (self.completed_tasks / self.assigned_tasks) * 100
        attendance_percentage = (self.total_attendance / 30) * 100  # Assuming 30 working days in a month

        # Penalty for leaves beyond 3
        leaves_penalty = max(0, self.total_leaves - 3)
        leave_percentage = max(0, 100 - (leaves_penalty * 3))  # Assuming a penalty of 3% for each leave beyond 3

        overall_performance = (task_performance + attendance_percentage + leave_percentage) / 3
        self.performance_percentage = overall_performance
        return overall_performance

def insert_employee_data(employee):
    insert_query = '''
    INSERT INTO employees (name, assigned_tasks, completed_tasks, total_attendance, total_leaves, performance_percentage)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (employee.name, employee.assigned_tasks, employee.completed_tasks,
                                  employee.total_attendance, employee.total_leaves, employee.calculate_performance()))
    conn.commit()

def main():
    st.title("Employee Performance Calculator")

    # Input for Excel file upload
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)  # For Excel files

            st.subheader("Uploaded Data:")
            st.table(df)

            employees = []
            for index, row in df.iterrows():
                employee = Employee(
                    name=row['name'],
                    assigned_tasks=row['assigned_tasks'],
                    total_attendance=row['total_attendance'],
                    total_leaves=row['total_leaves'],
                    completed_tasks=row['completed_tasks']
                )
                employees.append(employee)

            # Display consolidated table for all employees
            performance_data = []
            for i, employee in enumerate(employees):
                performance_percentage = employee.calculate_performance()
                performance_data.append({
                    'Employee Name': employee.name,
                    'Assigned Tasks': employee.assigned_tasks,
                    'Completed Tasks': employee.completed_tasks,
                    'Attendance Percentage': (employee.total_attendance / 30) * 100,
                    'Leaves Taken': employee.total_leaves,
                    'Performance Percentage': employee.performance_percentage
                })

            st.subheader("Consolidated Employee Performance Table:")
            st.table(performance_data)

            if st.button("Submit"):
                for employee in employees:
                    insert_employee_data(employee)
                st.success("Data submitted successfully!")

        except pd.errors.EmptyDataError:
            st.warning("Uploaded file is empty.")
        except pd.errors.ParserError:
            st.error("Error parsing the file. Please upload a valid Excel file.")

if __name__ == "__main__":
    main()
