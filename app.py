# 1. Import our tools
import streamlit as st  # This builds the website
from fpdf import FPDF   # This makes the PDF
import os               # This helps us save files on the computer

# 2. Create the "Face" of the app
st.title("💊 My Digital Doctor App")
st.write("Welcome, Doctor! Fill in the details below.")

# These are the boxes where the doctor types
doctor_name = st.text_input("Doctor Name", "Dr. Smith")
patient_name = st.text_input("Patient Name")
patient_number = st.text_input("Patient WhatsApp Number (with Country Code, e.g., +1234567890)")
medicines = st.text_area("List of Medicines (Dosage)")

# 3. What happens when we click the button?
if st.button("Generate & Send Prescription"):
    
    # Check if the doctor filled everything in
    if patient_name and medicines and patient_number:
        
        # --- PART A: CREATE THE PDF (The Brain) ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        
        # Writing on the "paper"
        pdf.cell(200, 10, txt=f"Prescription by {doctor_name}", ln=1, align='C')
        pdf.cell(200, 10, txt="---------------------------------------", ln=1, align='C')
        pdf.cell(200, 10, txt=f"Patient: {patient_name}", ln=1, align='L')
        pdf.ln(10) # Add an empty line
        pdf.multi_cell(0, 10, txt=f"Medicines:\n{medicines}")
        
        # Save the PDF file
        file_name = f"{patient_name}_prescription.pdf"
        pdf.output(file_name)
        st.success(f"Step 1 Done: PDF saved as {file_name}!")
        
        
        
    else:

        st.error("Please fill in all the details first!")

