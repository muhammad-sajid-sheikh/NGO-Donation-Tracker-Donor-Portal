from fpdf import FPDF
import os

class PDFReceipt(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Donation Receipt", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Thank you for your support!", align="C")

def create_pdf_receipt(donation_data, filename="receipt.pdf"):
    pdf = PDFReceipt()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for key, value in donation_data.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    
    output_path = os.path.join("data", filename)
    pdf.output(output_path)
    return output_path
