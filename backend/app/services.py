from fpdf import FPDF


def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)

    pdf_path = 'path/to/generated_contract.pdf'
    pdf.output(pdf_path)
    return pdf_path