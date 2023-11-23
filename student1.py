import streamlit as st

class Employee:
    def __init__(self, name, assigned_tasks):
        self.name = name
        self.assigned_tasks = assigned_tasks
        self.completed_tasks = 0

    def complete_task(self, tasks_completed):
        self.completed_tasks += tasks_completed

    def calculate_performance(self):
        return (self.completed_tasks / self.assigned_tasks) * 100

# Streamlit web application
def main():
    st.title("Employee Performance Calculator")

    # Input for employee details
    name = st.text_input("Enter Employee Name:")
    assigned_tasks = st.number_input("Enter Number of Assigned Tasks:", min_value=1, step=1)

    # Create an instance of the Employee class
    employee = Employee(name, assigned_tasks)

    # Input for completed tasks
    tasks_completed = st.number_input("Enter Number of Completed Tasks:", min_value=0, step=1)
    employee.complete_task(tasks_completed)

    # Display performance
    if assigned_tasks > 0:
        performance_percentage = employee.calculate_performance()
        st.write(f"Performance: {performance_percentage:.2f}%")

if __name__ == "__main__":
    main()
