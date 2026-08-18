from reportlab.pdfgen import canvas
from django.http import HttpResponse



def generate_receipt_pdf(receipt):

    response = HttpResponse(
        content_type="application/pdf"
    )


    response[
        "Content-Disposition"
    ] = (
        f'attachment; filename="'
        f'{receipt.receipt_number}.pdf"'
    )


    pdf = canvas.Canvas(response)


    payment = receipt.payment


    y = 800


    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        180,
        y,
        "CampusPay Enterprise"
    )


    y -= 40


    pdf.setFont(
        "Helvetica",
        12
    )


    lines = [

    f"Receipt Number: {receipt.receipt_number}",

    f"Student: {payment.member.full_name}",

    f"Student ID: {payment.member.student_id}",

    f"Department: {payment.member.department}",

    f"Academic Year: {payment.fee_structure.semester.academic_year}",

    f"Semester: {payment.fee_structure.semester}",

    f"Amount Paid: GH₵ {payment.amount_paid}",

    f"Payment Method: {payment.payment_method}",

    f"Date: {payment.payment_date.strftime('%d %B %Y')}",

]

    for line in lines:

        pdf.drawString(
            80,
            y,
            line
        )

        y -= 25


    pdf.save()


    return response