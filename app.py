import streamlit as st
from fpdf import FPDF
import io
import datetime
import base64 



st.title("👨‍⚕️ Digital Prescription Pad (Local Download & Shareable Link)")
st.write("Generate the PDF and copy the shareable link for the patient.")




date_of_visit = st.date_input("Day of Visit", datetime.date.today())


doctor_name = st.text_input("Doctor Name", "Dr. A. Guide")
patient_name = st.text_input("Patient Name")
medicines = st.text_area("List of Medicines & Instructions")
def create_prescription_pdf(doctor, patient, meds, visit_date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    
    
    pdf.cell(0, 10, txt=f"Official Prescription by {doctor}", ln=1, align='C')
    pdf.cell(0, 10, txt="---------------------------------------", ln=1, align='C')
    
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Patient Name: {patient}", ln=1, align='L')
    pdf.cell(0, 10, txt=f"Date of Visit: {visit_date.strftime('%B %d, %Y')}", ln=1, align='L')
    pdf.ln(5)
    
    
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt="Rx: Medications & Instructions", ln=1, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 7, txt=meds)
    
    
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    return pdf_bytes


# 2. Button Action
if st.button("Generate Prescription & Link"):
    if patient_name and medicines:
        try:
            
            pdf_bytes = create_prescription_pdf(
                doctor_name, 
                patient_name, 
                medicines, 
                date_of_visit
            )
            file_name = f"{patient_name.replace(' ', '_')}_Prescription.pdf"

            st.success("✅ PDF Generated. See download options below.")
            
            
            
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            download_link_data = f'data:application/pdf;base64,{base64_pdf}'

            st.markdown("---")
            st.markdown("### 🔗 Shareable Download Link")
            st.info("Copy this entire link and send it to the patient via WhatsApp or Email. When they click it, the download starts.")

            
            st.text_area(
                label="Copy this Link (Warning: it is very long!)",
                value=download_link_data,
                height=150
            )

            st.markdown("---")
            st.markdown("### 💾 Doctor's Local Download")
            
            st.download_button(
                label=f"⬇️ Download {file_name} to PC/Device",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            
    else:
        st.error("Please fill in the Patient Name and Medicines sections.")



