import streamlit as st

class Employee:
    def __init__(self, name, assigned_tasks):
        self.name = name
        self.assigned_tasks = assigned_tasks
        self.completed_tasks = 0

    def calculate_performance(self):
        if self.assigned_tasks == 0:
            return 0  # To avoid division by zero
        return (self.completed_tasks / self.assigned_tasks) * 100

# Streamlit UI
def main():
    st.title("Employee Performance Calculator")

    # Input details for multiple employees
    employees = []
    while st.button("Add Employee"):
        st.write(f"\n--- Employee {len(employees) + 1} ---")
        # User input for employee details
        name = st.text_input("Enter Employee Name:")
        assigned_tasks = st.number_input("Enter Number of Assigned Tasks:", min_value=0, step=1)

        # Create an instance of Employee
        employee = Employee(name, assigned_tasks)

        # User input for completed tasks
        completed_tasks = st.number_input("Enter Number of Completed Tasks:", min_value=0, step=1, max_value=employee.assigned_tasks)
        employee.completed_tasks = completed_tasks

        employees.append(employee)

    # Display employee performance in a table
    performance_list = []
    for i, employee in enumerate(employees, 1):
        performance = {
            "Employee": i,
            "Name": employee.name,
            "Assigned Tasks": employee.assigned_tasks,
            "Completed Tasks": employee.completed_tasks,
            "Performance (%)": employee.calculate_performance()
        }
        performance_list.append(performance)

    st.table(performance_list)

if __name__ == "__main__":
    main()

