# MIT License

#Copyright (c) 2018 Manjeet Singh Bhatia

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

  # The above copyright notice and this permission notice shall be included in all
     # copies or substantial portions of the Software.

     # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
     # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
     # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
     # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
     # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
     # SOFTWARE.

import PyPDF2
import argparse
from googletrans import Translator
from fpdf import FPDF
import os
import re
 
def check_if_file_exists(filepath):
    if not os.path.exists(filepath):
        print("File path %s doesn't exists", filepath)
        sys.exit()
    fileext = filepath.split(".")
    filext = fileext[len(fileext)-1]
    if filext != "pdf":
        print("File %s is not PDF file", filepath)
        sys.exit()
    return True

def convert_pdf_to_text(input_file):
    pdfFileObj = open(input_file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numPages = pdfReader.numPages
    return pdfReader,numPages,pdfFileObj


def strip_unicodes(book_data):
    book_data.replace('\xe2', '')
    book_data.replace('\xe2', '')
    book_data.replace('\x84', '')
    book_data.replace('\xa2', '')
    return book_data


def resseamble_words(page_data):
    lines = page_data.split(' \n')
    data = ''
    for line in lines:
        data += line.replace('\n', '')
    data.replace('....', '.')
    data.replace('...', '.')
    data = data.split(" ")
    org_data = ''
    for i in range(0, len(data)-1):
        if i%13 == 0:
            org_data += ' \n '
        org_data += data[i] + " "
    return org_data


def read_pages_from(pdfread, numPages):
    translator = Translator()
    Book_data=''
    for i in range(3, numPages):
        pageObj = pdfread.getPage(i)
        page_data = pageObj.extractText()
        page_datap = resseamble_words(page_data)
        translated_page = translator.translate(page_datap, dest='pa')
        Book_data += "---\n\n---" \
            + translated_page.text.encode('utf-8')
    return Book_data


def get_Book_data(input_file):
    pdfread, book_len, pdfFileObj = convert_pdf_to_text(input_file)
    book_data = read_pages_from(pdfread, book_len)
    pdfFileObj.close()
    return book_data


def strip_unicodes(book_data):
    book_data.replace('\u2122', '')
    #book_data.replace('\xe2', '')
    #book_data.replace('\x84', '')
    #book_data.replace('\xa2', '')
    return book_data


def write_to_pdf(input_file, outfile=None):
    book_data =  get_Book_data(input_file)
    if outfile is None:
        outo = input_file.split('.')
        outfile = outo[len(outo)-2] + '.txt'
    with open(outfile, 'wb') as ham:
        ham.write(book_data)
    book_data = strip_unicodes(book_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()                                               
    parser.add_argument("-f", "--file", type=str,
                        required=True, help="File path of pdf document")
    parser.add_argument("-o", "--outp", type=str,
                        required=False, help="Output File Path")
    args = parser.parse_args()
    outfile = args.outp or None
    filepath = args.file
    if check_if_file_exists(filepath):
        write_to_pdf(filepath, outfile)
