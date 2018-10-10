from fpdf import FPDF


def get_row(edit):
    addition = "Addition"
    if not edit.is_add:
        addition = "Deletion"
    return [edit.time, edit.file_name, addition, edit.content]


def format_date_from_datetime(dt_object):
    return "{0}-{1}-{2}".format(dt_object.day, dt_object.month, dt_object.year)


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


def generate_pdf_report2(user, start_time, end_time):

    start_date = format_date_from_datetime(start_time)
    end_date = format_date_from_datetime(end_time)

    # Letter size paper, use inches as unit of measure
    pdf = FPDF(format='letter', unit='in')

    # Add new page. Without this you cannot create the document.
    pdf.add_page()

    # Remember to always put one of these at least once.
    pdf.set_font('Arial', '', 10.0)

    # Effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin

    # Set column width to 1/4 of effective page width to distribute content
    # evenly across table and page
    col_width = epw / 3

    data = [get_row(edit) for edit in user.edits if start_time <= edit.time <= end_time]
    # Document title centered, 'B'old, 14 pt
    pdf.set_font('Arial', 'B', 16.0)
    pdf.multi_cell(epw, 0.0, user.name)
    th = pdf.font_size

    pdf.set_font('Arial', '', 12.0)
    pdf.ln(2 * th)
    pdf.cell(0, 2 * th, "Contributions between {0} and {1}".format(start_date, end_date))
    pdf.ln(2 * th)

    pdf.set_font('Arial', '', 12.0)
    pdf.cell(0, 2 * th, "Number of characters added: {0}".format(user.num_added))
    pdf.ln()
    pdf.cell(0, 2 * th, "Number of characters deleted: {0}".format(user.num_deleted))
    pdf.ln(4 * th)

    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(0, 2 * th, "Format of edits")
    pdf.ln(2 * th)


    # Describe format of edit
    pdf.set_font('Arial', 'I', 12.0)
    pdf.cell(col_width, 2 * th, "Date and time", border=1)
    pdf.cell(col_width * 1.5, 2 * th, "File name", border=1)
    pdf.cell(col_width * 0.5, 2 * th, "Addition/Deletion", border=1)
    pdf.ln(2 * th)
    pdf.cell(0, 2 * th, "Content of edit", border=1)

    pdf.set_font('Arial', 'B', 14.0)
    pdf.ln(6 * th)
    pdf.cell(0, 2 * th, "Edit history")

    pdf.set_font('Arial', '', 12.0)
    pdf.ln(4 * th)
    for row in data:
        if pdf.h - pdf.y < pdf.b_margin + 4 * th:
            pdf.add_page()

        pdf.cell(col_width, 2 * th, str(row[0]), border=1)
        pdf.cell(col_width * 1.5, 2 * th, str(row[1]), border=1)
        pdf.cell(col_width * 0.5, 2 * th, str(row[2]), border=1)
        pdf.ln(2 * th)
        pdf.multi_cell(0, 2 * th, str(row[3]), border=1)

        pdf.ln(4 * th)

    try:
        pdf.output('{0} {1} to {2}.pdf'.format(user.name, start_date, end_date), 'F')
    except:
        # file already exists and is open
        pass



