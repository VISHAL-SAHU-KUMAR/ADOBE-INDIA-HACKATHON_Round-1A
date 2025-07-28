from fpdf import FPDF

def create_test_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 20, 'Test Document Title', ln=True, align='C')
    
    # H1 heading
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 20, '1. Introduction', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'This is some content text.', ln=True)
    
    # H2 heading
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 20, '1.1 Background', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Some background information.', ln=True)
    
    # H3 heading
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 20, '1.1.1 Detailed Section', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Detailed content here.', ln=True)
    
    pdf.output('input/test.pdf')

if __name__ == '__main__':
    create_test_pdf()
