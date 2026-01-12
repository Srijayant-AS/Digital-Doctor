import streamlit as st
from fpdf import FPDF
import io
import datetime
import base64

# --- 1. PROFESSIONAL PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Digital Doctor Pad", 
    page_icon="👨‍⚕️",
    layout="centered"
)

# --- 2. HIDE BRANDING & GITHUB MENU ---
# This CSS removes the Streamlit footer, header, and the GitHub redirect menu
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {display:none;} 
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 3. PDF GENERATION LOGIC ---
def create_prescription_pdf(doctor, patient, meds, visit_date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    
    # Header
    pdf.set_font("Arial", 'B', size=20)
    pdf.cell(0, 10, txt=f"{doctor}", ln=1, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 5, txt="Digital Prescription Record", ln=1, align='C')
    pdf.cell(0, 10, txt="---------------------------------------------------------------------------------", ln=1, align='C')
    
    # Body Info
    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(0, 10, txt=f"Date of Visit: {visit_date.strftime('%B %d, %Y')}", ln=1, align='R')
    pdf.cell(0, 10, txt=f"Patient Name: {patient}", ln=1, align='L')
    pdf.ln(10)
    
    # Prescription Title
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt="Rx / Medications & Instructions:", ln=1, align='L')
    
    # Medication Content
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, txt=meds)
    
    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", 'I', size=10)
    pdf.cell(0, 10, txt="Generated via Digital Doctor Pad", ln=1, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- 4. APP INTERFACE ---

st.title("👨‍⚕️ Digital Doctor Pad")
st.write("Professional Prescription Management System")
st.markdown("---")

# Input Section
col1, col2 = st.columns(2)

with col1:
    doctor_name = st.text_input("Doctor Name", "Dr. A. Guide")
    patient_name = st.text_input("Patient Name")

with col2:
    date_of_visit = st.date_input("Day of Visit", datetime.date.today())

medicines = st.text_area("Prescription (Medicines, Dosage, and Duration)", height=150)

st.markdown("---")

# --- 5. ACTION BUTTON ---
if st.button("🚀 Generate Professional Prescription"):
    if patient_name and medicines:
        try:
            # Generate the file
            pdf_bytes = create_prescription_pdf(
                doctor_name, 
                patient_name, 
                medicines, 
                date_of_visit
            )
            file_name = f"{patient_name.replace(' ', '_')}_Prescription.pdf"

            st.success("✅ Prescription Successfully Generated!")

            # --- SHAREABLE LINK (Base64) ---
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            download_link_data = f'data:application/pdf;base64,{base64_pdf}'

            st.subheader("🔗 Patient Share Link")
            st.info("Click the icon in the top-right of the box below to copy the whole link.")
            
            # This 'st.code' block provides the seamless 'Copy' button automatically
            st.code(download_link_data, language=None)

            st.markdown("---")

            # --- LOCAL DOWNLOAD ---
            st.subheader("💾 Doctor's Archive")
            st.download_button(
                label="📥 Download Copy to this Device",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"❌ An error occurred during generation: {e}")
    else:
        st.warning("⚠️ Please enter the Patient Name and Medication details first.")





