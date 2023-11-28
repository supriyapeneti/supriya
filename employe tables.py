import streamlit as st
import psycopg2

# Define your PostgreSQL connection parameters

# Create a connection to the PostgreSQL database
conn = psycopg2.connect(
    database="employee", user='user', password='5001', host='127.0.0.1', port='5432'
)
cursor = conn.cursor()

# Create a table to store employee information if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    attendance INTEGER NOT NULL,
    productivity INTEGER NOT NULL,
    teamwork INTEGER NOT NULL,
    leave INTEGER NOT NULL,
    feedback TEXT,
    goals_achieved INTEGER NOT NULL,
    self_assessment INTEGER NOT NULL,
    performance_score INTEGER NOT NULL
);
'''
cursor.execute(create_table_query)
conn.commit()

# Added the sidebar
app_mode = st.sidebar.radio(
    "",
    ("Employee Perfomance Calculator", "Retrive data by Employee name"),
)

if app_mode == "Employee Perfomance Calculator":

    class Employee:
        def __init__(self, name, attendance, productivity, teamwork, leave, feedback=None, goals_achieved=0,
                     self_assessment=0):
            self.name = name
            self.attendance = attendance
            self.productivity = productivity
            self.teamwork = teamwork
            self.leave = leave
            self.feedback = feedback if feedback else "No feedback provided"
            self.goals_achieved = goals_achieved
            self.self_assessment = self_assessment
            self.performance_score = None  # Initialize performance_score

        def calculate_performance(self):
            # Define weights for each criterion
            attendance_weight = 0.2
            productivity_weight = 0.4
            teamwork_weight = 0.2
            leave_weight = 0.1
            goals_weight = 0.2
            self_assessment_weight = 0.1

            # Calculate overall performance score
            self.performance_score = (
                    self.attendance * attendance_weight +
                    self.productivity * productivity_weight +
                    self.teamwork * teamwork_weight -
                    self.leave * leave_weight +
                    self.goals_achieved * goals_weight +
                    self.self_assessment * self_assessment_weight
            )

            return self.performance_score


    # performance_app.py

    def insert_employee_data(employee):
        # Insert employee data into the database
        insert_query = '''
            INSERT INTO employees (name, attendance, productivity, teamwork, leave, feedback, goals_achieved, self_assessment, performance_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
        cursor.execute(insert_query, (employee.name, employee.attendance, employee.productivity, employee.teamwork,
                                      employee.leave, employee.feedback, employee.goals_achieved,
                                      employee.self_assessment,
                                      employee.calculate_performance()))  # Use calculate_performance() here
        conn.commit()


    def main():
        st.title("Employee Performance Calculator")

        # Get employee information from user input
        employee_name = st.text_input("Enter employee name:")
        attendance = st.slider("Attendance:", 0, 100, 50)
        productivity = st.slider("Productivity:", 0, 100, 50)
        teamwork = st.slider("Teamwork:", 0, 100, 50)
        leave = st.slider("Leave taken (days):", 0, 30, 0)
        feedback = st.text_area("Feedback:")
        goals_achieved = st.number_input("Number of goals achieved:", 0, 10, 0)
        self_assessment = st.slider("Self-assessment:", 0, 100, 50)

        # Create Employee instance
        employee = Employee(
            name=employee_name,
            attendance=attendance,
            productivity=productivity,
            teamwork=teamwork,
            leave=leave,
            feedback=feedback,
            goals_achieved=goals_achieved,
            self_assessment=self_assessment,
        )

        # Calculate button
        if st.button("Calculate"):
            # Calculate performance score
            performance_score = employee.calculate_performance()

            # Insert employee data into the database
            insert_employee_data(employee)

            # Display results
            st.subheader(f"{employee_name}'s Performance Score: {performance_score:.2f}")

            # Display additional information
            st.write(f"\nFeedback: {feedback}")
            st.write(f"Goals achieved: {goals_achieved}")
            st.write(f"Self-assessment score: {self_assessment}")
            st.write(f"Leave taken (days): {leave}")

if __name__ == "__main__":
    main()

# Close the database connection
cursor.close()
conn.close()
