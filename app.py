import streamlit as st
import os
from pypdf import PdfWriter

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="RGUHS B.Pharm PYQs", page_icon="🇮🇳", layout="centered")

# --- INDIAN FLAG BACKGROUND & STYLE (CSS) ---
# Is code me aapki bheji gayi flag image (72280.jpg) ka online link upyog kiya gaya hai
flag_theme_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://www.123freevectors.com/wp-content/original/210811-indian-flag-low-poly-background.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

/* Text style taaki tirange ke upar likhai bilkul saaf aur bold dikhe */
h1, h2, h3, p, span, label, div {
    color: #000000 !important; /* Bold Black Text */
    font-weight: bold !important;
    text-shadow: 1px 1px 2px #FFFFFF; /* White shadow taaki dark areas me bhi dikhe */
}

/* Button code - Navy Blue color jaise Ashok Chakra ka hota hai */
.stButton>button {
    background-color: #000080 !important;
    color: #ffffff !important;
    border-radius: 6px;
    border: 1px solid #000080;
    font-weight: bold;
}
</style>
"""
st.markdown(flag_theme_css, unsafe_allow_html=True)

# --- TITLE ---
st.title("🇮🇳 RGUHS B.Pharm PYQs")
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
    "Semester 4": [
        "Pharmaceutical_Organic_Chemistry_III",
        "Medicinal_Chemistry_I",
        "Physical_Pharmaceutics_II",
        "Pharmacology_I",
        "Pharmacognosy_I"
    ],
    "Semester 5": ["Not Available"],
    "Semester 6": ["Not Available"],
    "Semester 7": ["Not Available"],
    "Semester 8": ["Not Available"]
}

# --- DATA: YEARS LIST ---
years_list = [
    "November_2025",
    "May_2025",
    "November_2024",
    "May_2024",
    "November_2023",
    "May_2023",
    "November_2022",
    "May_2022",
    "November_2021",
    "May_2021",
    "November_2020"
]

# --- 1. SEMESTER SELECTION ---
selected_semester = st.selectbox("Select Semester:", list(semester_data.keys()))

# --- 2. SUBJECT SELECTION ---
current_subjects = semester_data[selected_semester]
selected_subjects = st.multiselect("Select Subjects:", current_subjects)

# --- 3. YEAR SELECTION ---
selected_years = st.multiselect("Select Year:", years_list)

# --- GENERATE PDF BUTTON ---
if st.button("Generate Combined PDF"):
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
                st.success(f"Success! {found_count} papers merged perfectly.")
                st.download_button(
                    label="Download Combined PDF",
                    data=f,
                    file_name="RGUHS_Combined_Papers.pdf",
                    mime="application/pdf"
                )
            
            if missing_files:
                st.warning(f"Note: The following files were not found: {missing_files}")
        else:
            st.error("No matching files found in the database.")
            st.info("Ensure filenames match format: Subject_Month_Year.pdf")
