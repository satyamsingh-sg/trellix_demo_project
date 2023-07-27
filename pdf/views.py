from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .models import Product
import PyPDF2
import io 
def product(request):
  if request.method == "POST":
    description = request.POST.get('comments')
    password = request.POST.get('password')
    pdffile = request.FILES.get('myfile')
    protected_pdf_content = protect_pdf_with_password(pdffile,password)
    name = pdffile.name
    if description is not None and pdffile is not None:
      product = Product.objects.create(description = description, password = password)
      save_protected_pdf(name[:-4], product, protected_pdf_content)
      return render(request, 'product.html',{'product': product})
    else:
      return HttpResponse('Please enter a description and upload a PDF file.')
  else:
    return render(request, 'product.html')


def protect_pdf_with_password(pdffile, password): 
    inputpdf = PyPDF2.PdfReader(pdffile)
    pages_no = inputpdf.pages
    pdf_writer = PyPDF2.PdfWriter()

    for i in range(len(pages_no)):
      inputpdf = PyPDF2.PdfReader(pdffile)
      pdf_writer.add_page(inputpdf.pages[i])
      pdf_writer.encrypt(password)
    output_stream = io.BytesIO()
    pdf_writer.write(output_stream)
    
    return output_stream.getvalue()

def save_protected_pdf(name, product, pdf_content):
    product.pdffile.save(name + "_protected.pdf" , io.BytesIO(pdf_content), save=True)
    
    
    
# file check (type of file)
# password protection
# filesize


