import streamlit as st
import os
from pypdf import PdfWriter

st.set_page_config(page_title="B.Pharm Paper Hub", page_icon="💊")
st.title("💊 B.Pharm Previous Year Papers")

# --- 1. SUBJECTS KI LIST (Naye Subject) ---
subjects = [
    "Pharmaceutical_Engineering",
    "Pharmaceutical_Microbiology",
    "Physical_Pharmaceutics_I",
    "Pharmaceutical_Organic_Chemistry_II”, 
    "HAP_2"
]

# --- 2. YEARS KI LIST (Month aur Year ke saath) ---
# Dhyan rahe: Filename me bhi same spelling aur underscore hona chahiye
years = [
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

st.write("Apna Subject aur Exam Session select karein 👇")

# --- SELECTION ---
selected_sub = st.multiselect("Select Subjects:", subjects)
selected_years = st.multiselect("Select Session (Year):", years)

# --- MERGE BUTTON ---
if st.button("Generate Combined PDF"):
    if not selected_sub or not selected_years:
        st.error("Please select at least one Subject and one Session!")
    else:
        merger = PdfWriter()
        found_count = 0
        missing_files = []
        
        # Files dhundhna
        for sub in selected_sub:
            for yr in selected_years:
                # File ka naam banaya ja raha hai
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
                st.success(f"Success! {found_count} papers merged. 🎉")
                st.download_button("📥 Download Combined PDF", f, "My_University_Papers.pdf")
            
            # Agar koi file nahi mili, toh user ko batao
            if missing_files:
                st.warning(f"Note: Ye files nahi mili: {missing_files}")
                
        else:
            st.error("❌ Koi bhi file match nahi hui. Please check filenames in GitHub.")
            st.write("Expected filename example: Pharmaceutical_Engineering_November_2020.pdf")

