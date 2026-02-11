import streamlit as st
import os
from pypdf import PdfWriter

st.set_page_config(page_title="Paper Hub", page_icon="📚")
st.title("📚 University Paper Downloader")

# --- SUBJECTS KI LIST ---
# भाई, यहाँ उन सब्जेक्ट्स के नाम लिखो जो आपके पास हैं
subjects = ["Pharmacology", "MedicinalChemistry", "Analysis"]
years = ["2020", "2021", "2022", "2023", "2024"]

st.write("Apna Subject aur Year select karo 👇")

# --- SELECTION ---
selected_sub = st.multiselect("Subjects:", subjects)
selected_years = st.multiselect("Years:", years)

# --- MERGE BUTTON ---
if st.button("Generate Combined PDF"):
    if not selected_sub or not selected_years:
        st.error("Pehle Subject aur Year select to karo bhai!")
    else:
        merger = PdfWriter()
        count = 0
        
        # Files dhundhna
        for sub in selected_sub:
            for yr in selected_years:
                filename = f"{sub}_{yr}.pdf"
                if os.path.exists(filename):
                    merger.append(filename)
                    count += 1
        
        # Download
        if count > 0:
            merger.write("Result.pdf")
            merger.close()
            
            with open("Result.pdf", "rb") as f:
                st.success(f"Badhai ho! {count} papers mil gaye.")
                st.download_button("📥 Download PDF", f, "Combined_Papers.pdf")
        else:
            st.error("Koi file nahi mili. Naam check karo (Example: Pharmacology_2023.pdf)")
