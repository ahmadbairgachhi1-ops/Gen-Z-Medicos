import streamlit as st
import os
from pypdf import PdfWriter

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="RGUHS B.Pharm PYQs", page_icon="🇮🇳", layout="centered")

# --- TRI-COLOR BOXES & BUTTON STYLE (CSS) ---
tricolor_theme_css = """
<style>
/* 1. Flag Background */
[data-testid="stAppViewContainer"] {
    background-image: url("https://raw.githubusercontent.com/ahmadbairgachhi1-ops/Gen-Z-Medicos/main/72280_2.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

/* Base Text settings */
h1, h2, h3, p, span, label, div {
    color: #000000 !important; 
    font-weight: bold !important;
    text-shadow: 1px 1px 2px #FFFFFF; 
}

/* 2. FIRST BOX (Semester Selectbox) -> SAFFRON */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #FF9933 !important; /* Saffron */
    border: 2px solid #FF9933 !important;
    color: #000000 !important;
    border-radius: 6px;
}

# --- 3. MULTISELECT BOXES GENERAL STYLE ---
/* Selected items inside ALL boxes (Navy Blue like Ashok Chakra) */
div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #000080 !important; 
    color: #FFFFFF !important;
}
div[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {
    color: #FFFFFF !important;
}

/* 4. SECOND BOX (Subject Container) -> WHITE */
div[data-testid="stMultiSelect"]:nth-of-type(1) {
    background-color: rgba(255, 255, 255, 0.95) !important; /* Pure White Box */
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 15px;
    border: 1px solid #E0E0E0;
}
div[data-testid="stMultiSelect"]:nth-of-type(1) div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
}

/* 5. THIRD BOX (Year Container) -> FIXED INDIAN FLAG GREEN */
/* Pukka aur sateek CSS rasta specifically 3rd box ke liye */
div[data-testid="stForm"] div[data-testid="stMultiSelect"]:nth-of-type(2),
div[data-testid="stAppViewContainer"] div[data-testid="stMultiSelect"]:nth-of-type(2),
.stMultiSelect:nth-child(3),
div[data-testid="stMultiSelect"] + div[data-testid="stMultiSelect"] {
    background-color: #138808 !important; /* Pure India Green */
    border-radius: 8px;
    padding: 12px;
    border: 1px solid #138808;
}
/* Year box ke andar wale select area ko bhi green ka touch dena */
div[data-testid="stMultiSelect"]:nth-of-type(2) div[data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
}

/* 6. ROUND WHITE BUTTON WITH NAVY BLUE BORDER */
.stButton>button {
    background-color: #FFFFFF !important; 
    color: #000080 !important; /* Navy Blue text */
    border-radius: 30px !important; /* Completely Rounded */
    border: 3px solid #000080 !important; /* Ashok Chakra Blue Border */
    font-weight: bold !important;
    padding: 12px 32px !important;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

/* Button hover effect */
.stButton>button:hover {
    background-color: #000080 !important; 
    color: #FFFFFF !important; 
}
</style>
"""
st.markdown(tricolor_theme_css, unsafe_allow_html=True)

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

# --- 1. SEMESTER SELECTION (Saffron) ---
selected_semester = st.selectbox("Select Semester:", list(semester_data.keys()))

# --- 2. SUBJECT SELECTION (White) ---
current_subjects = semester_data[selected_semester]
selected_subjects = st.multiselect("Select Subjects:", current_subjects)

# --- 3. YEAR SELECTION (Green) ---
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
