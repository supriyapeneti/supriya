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

    def calculate_task_performance(self):
        return (self.completed_tasks / self.assigned_tasks) * 100 if self.assigned_tasks > 0 else 0

    def calculate_attendance_performance(self):
        return (self.total_attendance / 30) * 100

    def calculate_leave_performance(self):
        # Penalty for leaves beyond 3
        leaves_penalty = max(0, self.total_leaves - 3)
        leave_percentage = max(0, 100 - (leaves_penalty * 5))  # Assuming a penalty of 5% for each leave beyond 3
        return leave_percentage

    def calculate_overall_performance(self):
        task_performance = self.calculate_task_performance()
        attendance_performance = self.calculate_attendance_performance()
        leave_performance = self.calculate_leave_performance()
        overall_performance = (task_performance + attendance_performance + leave_performance) / 3
        return overall_performance

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

        employee = Employee(name, assigned_tasks, total_attendance, total_leaves)
        employees.append(employee)

    # Display individual performance for each employee
    for i, employee in enumerate(employees):
        st.write(f"\n**Employee {i+1} - {employee.name}**")

        # Task Performance
        st.subheader("Task Performance:")
        task_performance_data = {
            'Completed Tasks': [employee.completed_tasks],
            'Assigned Tasks': [employee.assigned_tasks],
            'Task Performance Percentage': [employee.calculate_task_performance()]
        }
        st.table(task_performance_data)

        # Attendance Performance
        st.subheader("Attendance Performance:")
        attendance_performance_data = {
            'Total Attendance Days': [employee.total_attendance],
            'Attendance Percentage': [employee.calculate_attendance_performance()]
        }
        st.table(attendance_performance_data)

        # Leave Performance
        st.subheader("Leave Performance:")
        leave_performance_data = {
            'Total Leaves Taken': [employee.total_leaves],
            'Leave Performance Percentage': [employee.calculate_leave_performance()]
        }
        st.table(leave_performance_data)

        # Overall Performance
        st.subheader("Overall Performance:")
        overall_performance_data = {
            'Overall Performance Percentage': [employee.calculate_overall_performance()]
        }
        st.table(overall_performance_data)

if __name__ == "__main__":
    main()
