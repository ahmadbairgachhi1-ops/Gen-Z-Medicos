import streamlit as st
import os
from pypdf import PdfWriter

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Sci-Fi Paper Hub", page_icon="🚀", layout="centered")

# --- 2. SCI-FI ANIMATION & STYLE (CSS) ---
# Ye code background me chalne wala video/GIF lagayega
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://i.giphy.com/media/U3qYN8S0j3bpK/giphy.gif");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

/* Text ko white color dena taki dark background pe dikhe */
h1, h2, h3, p, div, span, label {
    color: #FFFFFF !important;
    text-shadow: 2px 2px 4px #000000;
}
.stMultiSelect div div {
    background-color: rgba(0, 0, 0, 0.5); /* Dropdown ko thoda transparent kala rang */
    color: white;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- 3. TITLE ---
st.title("🚀 B.Pharm Paper Hub (Sci-Fi Edition)")
st.write("Apna Subject aur Session select karein 👇")

# --- 4. SUBJECTS LIST (Aapki purani list) ---
subjects = [
    "Pharmaceutical_Engineering",
    "Pharmaceutical_Microbiology",
    "Physical_Pharmaceutics_I",
    "Pharmaceutical_Organic_Chemistry_II",
    "Pharmaceutical_Organic_Chemistry_I",
    "HAP_II",
    "Biochemistry",
    "Pathophysiology"
]

# --- 5. YEARS LIST (Aapki purani list) ---
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

# --- 6. SELECTION BOXES ---
selected_sub = st.multiselect("Select Subjects (Subject chunein):", subjects)
selected_years = st.multiselect("Select Session (Saal chunein):", years)

# --- 7. MERGE LOGIC ---
if st.button("🧬 Generate Combined PDF"):
    if not selected_sub or not selected_years:
        st.error("⚠️ Please select at least one Subject and one Session!")
    else:
        merger = PdfWriter()
        found_count = 0
        missing_files = []
        
        # Files dhundhna
        for sub in selected_sub:
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
                st.success(f"✅ Mission Successful! {found_count} papers merged.")
                st.download_button("📥 Download Combined PDF", f, "My_University_Papers.pdf")
            
            if missing_files:
                st.warning(f"⚠️ Ye files database me nahi mili: {missing_files}")
                
        else:
            st.error("❌ Error: Files not found.")
            st.info("Ensure filenames match format: Subject_Month_Year.pdf")

