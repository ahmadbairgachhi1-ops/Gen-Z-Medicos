import streamlit as st
import os
from pypdf import PdfWriter

# --- PAGE CONFIGURATION (Professional & Clean) ---
st.set_page_config(page_title="RGUHS B.Pharm PYQs", page_icon="📚", layout="centered")

# --- TITLE ---
st.title("RGUHS B.Pharm PYQs")
st.write("Select your Semester, Subjects, and Year to download the combined PDF.")

# --- DATA: SEMESTER & SUBJECTS MAPPING ---
semester_data = {
    "Semester 1": [
        "Pharmaceutical_Analysis_I",
        "Pharmaceutics_I",
        "HAP_I",
        "Pharmaceutical_Inorganic_Chemistry"
    ],
    "Semester 2": [
        "Pathophysiology",
        "Pharmaceutical_Organic_Chemistry_I",
        "Biochemistry",
        "HAP_II"
    ],
    "Semester 3": [
        "Pharmaceutical_Microbiology",
        "Physical_Pharmaceutics_I",
        "Pharmaceutical_Engineering",
        "Pharmaceutical_Organic_Chemistry_II"
    ],
    # Semesters 4 to 8 (Currently Not Available)
    "Semester 4": ["Not Available"],
    "Semester 5": ["Not Available"],
    "Semester 6": ["Not Available"],
    "Semester 7": ["Not Available"],
    "Semester 8": ["Not Available"]
}

# --- DATA: YEARS LIST ---
years_list = [
    "November_2020",
    "May_2021",
    "November_2021",
    "May_2022",
    "November_2022",
    "May_2023",
    "November_2023",
    "May_2024",
    "November_2024",
    "May_2025",
    "November_2025"
]

# --- 1. SEMESTER SELECTION (Box 1) ---
selected_semester = st.selectbox("Select Semester:", list(semester_data.keys()))

# --- 2. SUBJECT SELECTION (Box 2 - Dynamic) ---
# This list updates automatically based on the selected semester
current_subjects = semester_data[selected_semester]
selected_subjects = st.multiselect("Select Subjects:", current_subjects)

# --- 3. YEAR SELECTION (Box 3) ---
selected_years = st.multiselect("Select Year:", years_list)

# --- GENERATE PDF BUTTON ---
if st.button("Generate Combined PDF"):
    # Validation Logic
    if "Not Available" in selected_subjects:
        st.error("Subjects for this semester are not available yet.")
    elif not selected_subjects:
        st.error("Please select at least one Subject.")
    elif not selected_years:
        st.error("Please select at least one Year.")
    else:
        merger = PdfWriter()
        found_count = 0
        missing_files = []

        # Processing Files
        for sub in selected_subjects:
            for yr in selected_years:
                # Filename Format: Subject_Month_Year.pdf
                filename = f"{sub}_{yr}.pdf"
                
                if os.path.exists(filename):
                    merger.append(filename)
                    found_count += 1
                else:
                    missing_files.append(filename)
        
        # Download Section
        if found_count > 0:
            output_filename = "Combined_Papers.pdf"
            merger.write(output_filename)
            merger.close()
            
            with open(output_filename, "rb") as f:
                st.success(f"Success! {found_count} papers merged.")
                st.download_button(
                    label="Download Combined PDF",
                    data=f,
                    file_name="RGUHS_Combined_Papers.pdf",
                    mime="application/pdf"
                )
            
            # Show missing files warning if any
            if missing_files:
                st.warning(f"Note: The following files were not found: {missing_files}")
        else:
            st.error("No files found matching your selection.")
            st.info("Please ensure the files are uploaded to GitHub with the correct names.")

