import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    assigned_tasks = Column(Integer)
    completed_tasks = Column(Integer)
    total_attendance = Column(Integer)
    total_leaves = Column(Integer)

# Database setup
DATABASE_URL = "sqlite:///.desktop/employee_performance.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Streamlit web application with individual performance tables
def main():
    st.title("Employee Performance Calculator")

    # Input for multiple employees
    num_employees = st.number_input("Enter Number of Employees:", min_value=1, step=1)

    employees = []
    for i in range(num_employees):
        name = st.text_input(f"Enter Employee {i+1} Name:")
        assigned_tasks = st.number_input(f"Enter Number of Assigned Tasks for Employee {i+1}:", min_value=1, step=1)
        total_attendance = st.number_input(f"Enter Total Attendance (in days) for Employee {i+1}:", min_value=0, max_value=30, step=1)
        total_leaves = st.number_input(f"Enter Total Leaves (in days) for Employee {i+1}:", min_value=0, max_value=30, step=1)

        employee = Employee(name=name, assigned_tasks=assigned_tasks, total_attendance=total_attendance, total_leaves=total_leaves)
        employees.append(employee)

    # Display individual performance for each employee
    for i, employee in enumerate(employees):
        st.write(f"\n**Employee {i+1} - {employee.name}**")

        # Task Performance
        st.subheader("Task Performance:")
        task_performance_data = {
            'Metric': ['Completed Tasks', 'Assigned Tasks', 'Task Performance Percentage'],
            'Value': [0, employee.assigned_tasks, 0]
        }
        st.table(task_performance_data)

        # Attendance Performance
        st.subheader("Attendance Performance:")
        attendance_performance_data = {
            'Metric': ['Total Attendance Days', 'Attendance Percentage'],
            'Value': [employee.total_attendance, 0]
        }
        st.table(attendance_performance_data)

        # Leave Performance
        st.subheader("Leave Performance:")
        leave_performance_data = {
            'Metric': ['Total Leaves Taken', 'Leave Performance Percentage'],
            'Value': [employee.total_leaves, 0]
        }
        st.table(leave_performance_data)

        # Overall Performance
        st.subheader("Overall Performance:")
        overall_performance_data = {
            'Metric': ['Overall Performance Percentage'],
            'Value': [0]
        }
        st.table(overall_performance_data)

        # Store employee data in the database
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = Session()
        session.add(employee)
        session.commit()
        session.close()

    # Save data to Excel file
    df = pd.DataFrame([employee.__dict__ for employee in employees])
    df.to_excel("employee_data.xlsx", index=False)

if __name__ == "__main__":
    main()
