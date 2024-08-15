from fpdf import FPDF

def validate_signup(data):
    # Simple validation example
    if not data['name'] or not data['email'] or not data['username']:
        return "Missing required fields"
    if data['password1'] != data['password2']:
        return "Passwords do not match"
    return None


def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)

    file_path = 'static/contracts/generated_contract.pdf'
    pdf.output(file_path)
    return file_path