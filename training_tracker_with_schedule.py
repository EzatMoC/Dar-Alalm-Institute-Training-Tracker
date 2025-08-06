
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Training Tracker + Schedule", layout="wide")

# Predefined fields of study
predefined_fields = [
    "AI", "AI in Cybersecurity", "Cybersecurity", "AI in HR", "AI in BA",
    "AI in Stock Exchange", "AI in Graphic Design", "AI in Video & Image Editing",
    "Computer Skills", "AI in Smart & Sustainable Agriculture", "AI Models Development",
    "Data Entry", "Interior Design", "UAT", "Python", "Data Analysis",
    "AI in Organizations & Institutes Development", "Digital Transformation Using AI"
]

# Weekly schedule template (editable)
schedule = {
    "Saturday": {
        "7-8": ("AI in HR", "Round 1"),
        "8-9": ("Cybersecurity", "Round 2"),
    },
    "Sunday": {
        "7-8": ("AI in BA", "Round 3"),
        "8-9": ("Python", "Round 1"),
    },
    "Monday": {
        "7-8": ("Data Entry", "Round 4"),
        "8-9": ("AI in Stock Exchange", "Round 2"),
    },
    "Tuesday": {
        "7-8": ("AI", "Round 1"),
        "8-9": ("Interior Design", "Round 1"),
    },
    "Wednesday": {
        "7-8": ("AI in Graphic Design", "Round 2"),
        "8-9": ("AI in HR", "Round 2"),
    },
    "Thursday": {
        "7-8": ("Cybersecurity", "Round 3"),
        "8-9": ("AI in Smart & Sustainable Agriculture", "Round 1"),
    }
}

# Initialize trainee state
if "trainees" not in st.session_state:
    st.session_state.trainees = pd.DataFrame(columns=[
        "Name", "Email", "Phone", "Field of Study", "Round",
        "Enrollment Date", "Graduation Date", "Total Lectures", "Lectures Attended", "Lectures Remaining"
    ])

menu = st.sidebar.radio("Menu", ["➕ Enroll Trainee", "✅ Mark Attendance", "📊 View All Trainees", "📅 View Weekly Schedule"])

# Enroll trainee
if menu == "➕ Enroll Trainee":
    st.title("➕ Enroll New Trainee")
    with st.form("enroll_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            field = st.selectbox("Field of Study", options=predefined_fields + ["Other (type manually)"])
            if field == "Other (type manually)":
                field = st.text_input("Enter New Field of Study")
            round_info = st.text_input("Round (e.g. Round 3, Batch A)")
        with col2:
            enrollment_date = st.date_input("Enrollment Date", datetime.today())
            graduation_date = st.date_input("Expected Graduation Date")
            total_lectures = st.number_input("Total Lectures in Program", min_value=1, value=16)

        submit = st.form_submit_button("📥 Enroll Now")

        if submit:
            if name and email:
                new_row = {
                    "Name": name,
                    "Email": email,
                    "Phone": phone,
                    "Field of Study": field,
                    "Round": round_info,
                    "Enrollment Date": enrollment_date.strftime("%Y-%m-%d"),
                    "Graduation Date": graduation_date.strftime("%Y-%m-%d"),
                    "Total Lectures": total_lectures,
                    "Lectures Attended": 0,
                    "Lectures Remaining": total_lectures
                }
                st.session_state.trainees = pd.concat(
                    [st.session_state.trainees, pd.DataFrame([new_row])],
                    ignore_index=True
                )
                st.success(f"✅ Enrolled {name} in {field} ({round_info})")
            else:
                st.error("❗ Name and Email are required.")

# Attendance marking
elif menu == "✅ Mark Attendance":
    st.title("✅ Mark Lecture Attendance")
    if st.session_state.trainees.empty:
        st.warning("No trainees enrolled yet.")
    else:
        trainee_list = (
            st.session_state.trainees["Name"]
            + " - "
            + st.session_state.trainees["Field of Study"]
            + " (" + st.session_state.trainees["Round"] + ")"
        )
        selected = st.selectbox("Select trainee", trainee_list)
        index = trainee_list[trainee_list == selected].index[0]
        trainee = st.session_state.trainees.loc[index]

        st.subheader(f"Trainee: {trainee['Name']}")
        st.write(f"Field: {trainee['Field of Study']}, Round: {trainee['Round']}")
        st.write(f"Lectures Attended: {trainee['Lectures Attended']} / {trainee['Total Lectures']}")
        st.write(f"Lectures Remaining: {trainee['Lectures Remaining']}")

        if st.button("✅ Mark One Lecture Attended"):
            if trainee["Lectures Attended"] < trainee["Total Lectures"]:
                st.session_state.trainees.at[index, "Lectures Attended"] += 1
                st.session_state.trainees.at[index, "Lectures Remaining"] -= 1
                st.success("✅ Attendance updated")
            else:
                st.info("🎉 This trainee has already completed all lectures.")

# All trainees
elif menu == "📊 View All Trainees":
    st.title("🎓 All Enrolled Trainees")
    if st.session_state.trainees.empty:
        st.info("No trainee records yet.")
    else:
        st.dataframe(st.session_state.trainees, use_container_width=True)
        st.download_button(
            label="📥 Download CSV",
            data=st.session_state.trainees.to_csv(index=False),
            file_name="training_tracker.csv",
            mime="text/csv"
        )

# 📅 Weekly schedule view
elif menu == "📅 View Weekly Schedule":
    st.title("📅 Weekly Training Schedule")
    for day, slots in schedule.items():
        st.subheader(f"📆 {day}")
        for time_slot, (lecture_field, lecture_round) in slots.items():
            with st.expander(f"{time_slot} — {lecture_field} ({lecture_round})"):
                filtered = st.session_state.trainees[
                    (st.session_state.trainees["Field of Study"] == lecture_field) &
                    (st.session_state.trainees["Round"] == lecture_round)
                ]
                if filtered.empty:
                    st.write("No trainees enrolled in this session.")
                else:
                    st.dataframe(filtered[["Name", "Email", "Phone", "Lectures Attended", "Lectures Remaining"]])
