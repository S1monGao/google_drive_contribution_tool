from fpdf import FPDF


def generate_pdf_report(user):
    """

    :param user: User class instance
    :return: None
    :postcondition: Creates a pdf report for a given user
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, user.name)
    pdf.ln()
    pdf.set_font('Arial', '', 12)
    pdf.cell(40, 10, "Number of chars added: {0}".format(user.num_added))
    pdf.ln()
    pdf.cell(40, 10, "Number of chars deleted: {0}".format(user.num_deleted))
    pdf.ln()
    edits_string = ""
    for edit in user.edits:
        if edit.is_add:
            edit_string = "At {0}, User added: {1}\n".format(edit.time, edit.content)
        else:
            edit_string = "At {0}, User deleted: {1}\n".format(edit.time, edit.content)
        edits_string += edit_string
    pdf.multi_cell(0, 10, edits_string)
    pdf_name = user.name + '.pdf'
    pdf.output(pdf_name, 'F')
