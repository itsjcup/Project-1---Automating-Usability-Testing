import streamlit as st
import pandas as pd
import time
import os

# Create a folder called data in the main project folder
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define CSV file paths for each part of the usability testing
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASK_CSV = os.path.join(DATA_FOLDER, "task_data.csv")
EXIT_CSV = os.path.join(DATA_FOLDER, "exit_data.csv")


def save_to_csv(data_dict, csv_file):
    # Convert dict to DataFrame with a single row
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        # If CSV doesn't exist, write with headers
        df_new.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        # Else, we need to append without writing the header!
        df_new.to_csv(csv_file, mode='a', header=False, index=False)


def load_from_csv(csv_file):
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()


def main():
    st.title("Usability Testing Tool")

    home, consent, demographics, tasks, exit, report = st.tabs(
        ["Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"])

    with home:
        st.header("Introduction")
        st.write("""
        Welcome to the Usability Testing Tool for HCI.

        In this app, you will:
        1. Provide consent for data collection.
        2. Fill out a short demographic questionnaire.
        3. Perform a specific task (or tasks).
        4. Answer an exit questionnaire about your experience.
        5. View a summary report (for demonstration purposes).
        """)

    with consent:
        st.header("Consent Form")
        st.write("Please read the consent bellow  and agree to the agreement.")
        st.write("*Consent Agreement:*")
        st.write("""
                By participating, you agree to allow your responses and feedback 
                during the questionare to be recorded and used for research purposes only. 
                No personal information will be shared to the public.
                """)
        st.write("- I acknowledge my data will be used for research purposes.")
        st.write("- I acknowledge my information will not be shared to the public")
        consent_given = st.checkbox("I agree to the consent above")

        if st.button("Submit Consent"):
            if not consent_given:
                st.error("You must agree to the consent terms before proceeding.")

            else:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "consent_given": consent_given
                }
                save_to_csv(data_dict, CONSENT_CSV)
                st.success("Consent submitted")

    with demographics:
        st.header("Demographic Questionnaire")

        with st.form("demographic_form"):
            name = st.text_input("Enter full name", placeholder="First name and last name")
            age = st.number_input("Enter age", min_value=18, max_value=60, step=1)
            occupation = st.text_input("Enter occupation")
            familiarity = st.selectbox("Enter familiarity", options =
                                   ["", "Not Familiar", "Somewhat Familiar", "Familiar"])
            submitted = st.form_submit_button("Submit")

            missing = False

            if  age and name and occupation and familiarity:
                missing = True

            if submitted and missing:
                st.success("Demographic questionnaire submitted")
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "age": age,
                    "occupation": occupation,
                    "familiarity": familiarity
                }
                save_to_csv(data_dict, DEMOGRAPHIC_CSV)

            else:
                st.error("Please fill out the form, make sure all fields are completed")

    with tasks:
        st.header("Task Page")

        # Define available tasks and their descriptions
        task_options = {
            "Task 1: Example 1": "Press the Start Task Timer to begin.",
            "Task 2: Do Homework": "Records how long it takes to do homework.",
            "Task 3: Break Time": "Records how long user takes breaks.",
        }

        selected_task = st.selectbox("Select Task", list(task_options.keys()))

        st.write(f"*Task Description:* {task_options[selected_task]}")

        # Start/Stop Task Timer
        col1, col2 = st.columns(2)
        with col1:
            start_button = st.button("Start Task Timer")
        with col2:
            stop_button = st.button("Stop Task Timer")

        if start_button:
            st.session_state["start_time"] = time.time()
            st.info("Task timer started. Complete your task and then click 'Stop Task Timer'.")

        if stop_button and "start_time" in st.session_state:
            duration = time.time() - st.session_state["start_time"]
            rounded_duration = round(duration, 2)
            st.session_state["task_duration"] = duration
            st.success(f"Task duration recorded: {rounded_duration} seconds")

        # Task outcome
        success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partial"])
        notes = st.text_area("Observer Notes")

        if st.button("Save Task Results"):
            duration_val = st.session_state.get("task_duration", None)

            task_name = selected_task.split(":")[0].strip()

            data_dict = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "task_name": task_name,
                "success": success,
                "duration_seconds": round(duration_val, 2) if duration_val else "",
                "notes": notes
            }

            save_to_csv(data_dict, TASK_CSV)
            st.success("Task results saved.")

            # Clear session state
            st.session_state.pop("start_time", None)
            st.session_state.pop("task_duration", None)

    with exit:
        st.header("Exit Questionnaire")

        with st.form("exit_form"):
            # TODO: likert scale or other way to have an exit questionnaire

            satisfaction = st.radio(
                "Overall Satisfaction:",
                [1, 2, 3, 4, 5],
                format_func=lambda x: {
                    1: "Very Dissatisfied",
                    2: "Dissatisfied",
                    3: "Neutral",
                    4: "Satisfied",
                    5: "Very Satisfied"
                }[x]
            )

            difficulty = st.radio(
                "Overall Difficulty:",
                [1, 2, 3, 4, 5],
                format_func=lambda x: {
                    1: "Very Easy",
                    2: "Easy",
                    3: "Neutral",
                    4: "Difficult",
                    5: "Very Difficult"
                }[x]
            )

            open_feedback = st.text_area("Any additional comments or feedback?")

            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
            if submitted_exit:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "satisfaction": satisfaction,
                    "difficulty": difficulty,
                    "open_feedback": open_feedback
                }
                save_to_csv(data_dict, EXIT_CSV)
                st.success("Exit questionnaire data saved.")

    with report:
        st.header("Usability Report - Aggregated Results")

        # Consent Data
        st.subheader("Consent Data")
        consent_df = load_from_csv(CONSENT_CSV)
        if not consent_df.empty:
            st.dataframe(consent_df)
        else:
            st.info("No consent data available yet.")

        # Demographic Data
        st.subheader("Demographic Data")
        demographic_df = load_from_csv(DEMOGRAPHIC_CSV)
        if not demographic_df.empty:
            st.dataframe(demographic_df)
        else:
            st.info("No demographic data available yet.")

        # Task Data
        st.subheader("Task Performance Data")
        task_df = load_from_csv(TASK_CSV)
        if not task_df.empty:
            st.dataframe(task_df)

            # Bar chart of task success distribution
            st.markdown("**Task Completion Outcomes**")
            success_counts = task_df["success"].value_counts()
            st.bar_chart(success_counts)

            # Average duration per task
            if "duration_seconds" in task_df.columns:
                duration_means = task_df.groupby("task_name")["duration_seconds"].mean()
                st.markdown("**Average Task Duration (seconds)**")
                st.bar_chart(duration_means)

        else:
            st.info("No task data available yet.")

        # Exit Questionnaire Data
        st.subheader("Exit Questionnaire Data")
        exit_df = load_from_csv(EXIT_CSV)
        if not exit_df.empty:
            st.dataframe(exit_df)

            # Likert bar charts
            st.markdown("**Satisfaction Distribution**")
            st.bar_chart(exit_df["satisfaction"].value_counts().sort_index())

            st.markdown("**Difficulty Distribution**")
            st.bar_chart(exit_df["difficulty"].value_counts().sort_index())

            # Averages
            st.markdown("**Average Ratings**")
            avg_satisfaction = exit_df["satisfaction"].mean()
            avg_difficulty = exit_df["difficulty"].mean()
            st.write(f"Average Satisfaction: {avg_satisfaction:.2f}")
            st.write(f"Average Difficulty: {avg_difficulty:.2f}")
        else:
            st.info("No exit questionnaire data available yet.")


if __name__ == "__main__":
    main()