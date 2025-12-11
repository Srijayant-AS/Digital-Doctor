import streamlit as st
from fpdf import FPDF
import base64
import io
import qrcode
from PIL import Image

# ----------------- APP SETUP -----------------

st.title("👨‍⚕️ Digital Prescription Pad (QR Code Delivery)")
st.write("Fill in the details. The patient will receive a QR code to scan for the PDF.")

# 1. Input Fields
doctor_name = st.text_input("Doctor Name", "Dr. A. Guide")
patient_name = st.text_input("Patient Name")
medicines = st.text_area("List of Medicines & Instructions")

# Function to create the PDF file
def create_prescription_pdf(doctor, patient, meds):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    
    # Title and Doctor Info
    pdf.cell(0, 10, txt=f"Official Prescription by {doctor}", ln=1, align='C')
    pdf.cell(0, 10, txt="---------------------------------------", ln=1, align='C')
    
    # Patient Info
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Patient Name: {patient}", ln=1, align='L')
    pdf.ln(5)
    
    # Medicines
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt="Rx: Medications & Instructions", ln=1, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 7, txt=meds)
    
    # Save the PDF to a bytes object (The digital file content)
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    return pdf_bytes

# Function to generate QR code image
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the QR code image to a bytes object
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# 2. Button Action
if st.button("Generate Prescription & QR Code"):
    if patient_name and medicines:
        try:
            # A. Create the PDF file content
            pdf_bytes = create_prescription_pdf(doctor_name, patient_name, medicines)
            file_name = f"{patient_name.replace(' ', '_')}_Prescription.pdf"

            # B. Create the Magic Download Link (Base64 encoding)
            # This line turns the PDF bytes into a single piece of text that can be used as a link.
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            download_link_data = f'data:application/pdf;base64,{base64_pdf}'

            # C. Generate the QR Code
            qr_code_bytes = generate_qr_code(download_link_data)
            
            # D. Display Results
            st.success("✅ Prescription generated successfully!")
            
            st.markdown("### 📱 Patient Delivery Method:")
            st.info("Ask the patient to scan this code with their phone camera to download the PDF.")
            
            # Display the QR Code image
            st.image(qr_code_bytes, caption='Scan this code to download the Prescription', width=250)
            
            # Also display the PDF as a download button (Doctor's copy)
            st.download_button(
                label="Download PDF (Doctor's Copy)",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            
    else:
        st.error("Please fill in all the patient details.")
