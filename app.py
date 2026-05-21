# app.py

import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Hospital Patient Search System",
    layout="wide"
)

# -------------------------------
# SAMPLE PATIENT DATABASE
# -------------------------------

patients = [
    {"ID": 101, "Name": "Rahul", "Age": 22, "Disease": "Fever"},
    {"ID": 102, "Name": "Anjali", "Age": 25, "Disease": "Cold"},
    {"ID": 103, "Name": "Riya", "Age": 31, "Disease": "Diabetes"},
    {"ID": 104, "Name": "Karan", "Age": 28, "Disease": "Asthma"},
    {"ID": 105, "Name": "Sneha", "Age": 35, "Disease": "Migraine"},
    {"ID": 106, "Name": "Aman", "Age": 40, "Disease": "Heart Disease"},
    {"ID": 107, "Name": "Priya", "Age": 29, "Disease": "Typhoid"},
    {"ID": 108, "Name": "Rohit", "Age": 33, "Disease": "Malaria"},
    {"ID": 109, "Name": "Neha", "Age": 26, "Disease": "Dengue"},
    {"ID": 110, "Name": "Vikram", "Age": 45, "Disease": "Cancer"},
]

# SORTED DATA FOR BINARY SEARCH
patients_sorted = sorted(patients, key=lambda x: x["ID"])

# -------------------------------
# SEARCH FUNCTIONS
# -------------------------------

def linear_search(data, target):
    comparisons = 0

    start = time.time()

    for patient in data:
        comparisons += 1

        if patient["ID"] == target:
            end = time.time()
            return patient, comparisons, end - start

    end = time.time()
    return None, comparisons, end - start


def binary_search(data, target):
    left = 0
    right = len(data) - 1
    comparisons = 0

    start = time.time()

    while left <= right:
        comparisons += 1

        mid = (left + right) // 2

        if data[mid]["ID"] == target:
            end = time.time()
            return data[mid], comparisons, end - start

        elif data[mid]["ID"] < target:
            left = mid + 1

        else:
            right = mid - 1

    end = time.time()
    return None, comparisons, end - start


# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("🏥 Hospital System")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "View Patients",
        "Search Patient",
        "Performance Analysis"
    ]
)

# -------------------------------
# DASHBOARD
# -------------------------------

if menu == "Dashboard":

    st.title("🏥 Hospital Patient Search System")

    st.markdown("### Advanced Linear Search vs Binary Search Project")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Patients", len(patients))
    col2.metric("Search Algorithms", "2")
    col3.metric("System Status", "Active")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/2966/2966480.png",
        width=250
    )

    st.success("System Running Successfully")

# -------------------------------
# VIEW PATIENTS
# -------------------------------

elif menu == "View Patients":

    st.title("📋 Patient Records")

    df = pd.DataFrame(patients_sorted)

    st.dataframe(df, use_container_width=True)

# -------------------------------
# SEARCH PATIENT
# -------------------------------

elif menu == "Search Patient":

    st.title("🔍 Search Patient")

    patient_id = st.number_input(
        "Enter Patient ID",
        min_value=100,
        max_value=999,
        step=1
    )

    search_method = st.selectbox(
        "Choose Search Method",
        ["Linear Search", "Binary Search"]
    )

    if st.button("Search"):

        if search_method == "Linear Search":

            result, comparisons, search_time = linear_search(
                patients,
                patient_id
            )

        else:

            result, comparisons, search_time = binary_search(
                patients_sorted,
                patient_id
            )

        if result:

            st.success("Patient Found")

            st.write("### Patient Details")

            st.write(f"**Patient ID:** {result['ID']}")
            st.write(f"**Name:** {result['Name']}")
            st.write(f"**Age:** {result['Age']}")
            st.write(f"**Disease:** {result['Disease']}")

            st.info(f"Comparisons: {comparisons}")
            st.info(f"Search Time: {search_time:.10f} seconds")

        else:

            st.error("Patient Not Found")

# -------------------------------
# PERFORMANCE ANALYSIS
# -------------------------------

elif menu == "Performance Analysis":

    st.title("📊 Performance Analysis")

    test_id = st.number_input(
        "Enter Patient ID for Analysis",
        min_value=100,
        max_value=999,
        step=1
    )

    if st.button("Analyze"):

        linear_result, linear_comp, linear_time = linear_search(
            patients,
            test_id
        )

        binary_result, binary_comp, binary_time = binary_search(
            patients_sorted,
            test_id
        )

        st.subheader("Search Comparison")

        comparison_df = pd.DataFrame({
            "Algorithm": ["Linear Search", "Binary Search"],
            "Comparisons": [linear_comp, binary_comp],
            "Time": [linear_time, binary_time]
        })

        st.table(comparison_df)

        # GRAPH
        fig, ax = plt.subplots()

        ax.bar(
            ["Linear Search", "Binary Search"],
            [linear_comp, binary_comp]
        )

        ax.set_ylabel("Comparisons")
        ax.set_title("Linear vs Binary Search")

        st.pyplot(fig)

        # RESULT MESSAGE
        if linear_time > binary_time:
            st.success("Binary Search is Faster ✅")
        else:
            st.warning("Linear Search is Faster")

# -------------------------------
# FOOTER
# -------------------------------

st.markdown("---")
st.caption("Developed using Streamlit + Python")