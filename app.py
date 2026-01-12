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

# --- 2. THE "TOTAL CLOAK" CSS ---
# Hides: Hamburger menu, Footer, Header bar, Deploy button, Manage app widget, and status indicators.
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {display:none;}
            [data-testid="stStatusWidget"] {display: none;}
            [data-testid="stAppViewBlockContainer"] {padding-top: 2rem;}
            /* Disable the focus outline for a cleaner look */
            *:focus {outline: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 3. SESSION STATE FOR RESETTING FIELDS ---
# We use this to clear the form without refreshing the whole page.
if 'patient_name' not in st.session_state:
    st.session_state.patient_name = ""
if 'medicines' not in st.session_state:
    st.session_state.medicines = ""

def clear_form():
    st.session_state.patient_name = ""
    st.session_state.medicines = ""

# --- 4. PDF GENERATION LOGIC ---
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

# --- 5. APP INTERFACE ---

st.title("👨‍⚕️ Digital Doctor Pad")
st.write("Professional Prescription Management System")
st.markdown("---")

# Input Section
col1, col2 = st.columns(2)

with col1:
    # Doctor name stays saved in session by default
    doctor_name = st.text_input("Doctor Name", "Dr. A. Guide")
    # Patient name is linked to session state for clearing
    patient_name = st.text_input("Patient Name", key="patient_name")

with col2:
    date_of_visit = st.date_input("Day of Visit", datetime.date.today())

# Medicines area linked to session state
medicines = st.text_area("Prescription (Medicines, Dosage, and Duration)", height=150, key="medicines")

# --- 6. ACTION BUTTONS ---
btn_col1, btn_col2 = st.columns([3, 1])

with btn_col1:
    generate_pressed = st.button("🚀 Generate Professional Prescription", use_container_width=True)

with btn_col2:
    # Clicking this triggers the clear_form function
    if st.button("🗑️ Clear All", on_click=clear_form, use_container_width=True):
        st.toast("Fields cleared!")

st.markdown("---")

if generate_pressed:
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

            # --- SHAREABLE LINK ---
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            download_link_data = f'data:application/pdf;base64,{base64_pdf}'

            st.subheader("🔗 Patient Share Link")
            st.info("Copy the link below and send it to the patient.")
            
            # Displays the link with a built-in 'Copy' button
            st.code(download_link_data, language=None)

            # --- LOCAL DOWNLOAD ---
            st.subheader("💾 Doctor's Archive")
            st.download_button(
                label="📥 Download Copy to this Device",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter the Patient Name and Medication details.")






