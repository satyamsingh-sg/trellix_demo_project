from django.shortcuts import render
from django.http import HttpResponse 
import PyPDF2
import io 
import magic

def product(request):
    if request.method == "POST":
        password = request.POST.get('password')
        pdffile = request.FILES.get('myfile')

        if not pdffile:  
            return render(request, 'product.html', {'message': 'File field should not be empty.'})
        
        # Use python-magic to check the file format
        file_format = magic.from_buffer(pdffile.read(), mime=True)
        if file_format != 'application/pdf':
            return render(request, 'product.html', {'message': 'Invalid file format. Only PDF files are allowed.'})

        name = pdffile.name
        file_mb = pdffile.size / (1024 * 2024)

        if file_mb > 2:
            return render(request, 'product.html', {'message': 'File size must be less than 2 MB.'})

        if not (5 < len(password) < 10):
            return render(request, 'product.html', {'message': 'Password must be greater than 5 and less than 10 characters.'})
        
        protected_pdf_content = protect_pdf_with_password(pdffile, password)
        response = save_protected_pdf(name[:-4], protected_pdf_content)
        return response

    else:
        return render(request, 'product.html')

def protect_pdf_with_password(pdffile, password): 
    inputpdf = PyPDF2.PdfReader(pdffile)
    pdf_writer = PyPDF2.PdfWriter()

    for page in inputpdf.pages:
        pdf_writer.add_page(page)
        pdf_writer.encrypt(password)

    output_stream = io.BytesIO()
    pdf_writer.write(output_stream)
    return output_stream.getvalue()

def save_protected_pdf(name, pdf_content):
    protected_file = io.BytesIO(pdf_content)
    response = HttpResponse(FileWrapper(protected_file), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{name}_protect.pdf"'
    return response
