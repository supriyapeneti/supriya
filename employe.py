import streamlit as st

class Employee:
    def __init__(self, name, assigned_tasks, total_attendance, total_leaves):
        self.name = name
        self.assigned_tasks = assigned_tasks
        self.completed_tasks = 0
        self.total_attendance = total_attendance
        self.total_leaves = total_leaves

    def complete_task(self, tasks_completed):
        self.completed_tasks += tasks_completed

    def calculate_performance(self):
        task_performance = (self.completed_tasks / self.assigned_tasks) * 100
        attendance_percentage = (self.total_attendance / 30) * 100  # Assuming 30 working days in a month
        
        # Penalty for leaves beyond 3
        leaves_penalty = max(0, self.total_leaves - 3)
        leave_percentage = max(0, 100 - (leaves_penalty * 5))  # Assuming a penalty of 5% for each leave beyond 3
        
        overall_performance = (task_performance + attendance_percentage + leave_percentage) / 3
        return overall_performance

# Streamlit web application with table and pie chart
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

        employee = Employee(name, assigned_tasks, total_attendance, total_leaves)
        employees.append(employee)

    # Display performance for each employee
    for i, employee in enumerate(employees):
        st.write(f"\n**Employee {i+1} - {employee.name}**")
        st.table({
            'Name': [employee.name],
            'Assigned Tasks': [employee.assigned_tasks],
            'Completed Tasks': [employee.completed_tasks],
            'Attendance Percentage': [(employee.total_attendance / 30) * 100],
            'Leaves Taken': [employee.total_leaves],
            'Performance Percentage': [employee.calculate_performance()]
        })

    # Pie chart for overall performance
    overall_performances = [employee.calculate_performance() for employee in employees]
    labels = [f"Employee {i+1}" for i in range(num_employees)]
    st.write("\n**Overall Performance Pie Chart**")
    st.pie_chart(overall_performances, labels=labels)

if __name__ == "__main__":
    main()
