# MIT License

#Copyright (c) 2017 Manjeet Singh Bhatia

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

import argparse
from gtts import gTTS
import os
import PyPDF2
import re
import sys
 
def convert_pdf_to_text(filepath):
    pdfFileObj = open(filepath, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numPages = pdfReader.numPages
    return pdfReader,numPages,pdfFileObj

def strip_unicodes(page_data):
    page_data = page_data.replace('\xe2', '')
    page_data = page_data.replace('\xe2', '')
    page_data = page_data.replace('\x84', '')
    page_data = page_data.replace('\xa2', '')
    page_data = page_data.replace('\xc5', '')
    page_data = page_data.replace('\xc2', '')
    page_data = page_data.replace('\x81', '')
    page_data = page_data.replace('\xa3', '')
    page_data = page_data.replace('\xac', '')
    page_data = page_data.replace('\x82', '')
    page_data = page_data.replace('\xc3', '')
    page_data = page_data.replace('\xa9', '')
    page_data = page_data.replace('\xef', '')
    page_data = page_data.replace('-', ' ')
    page_data = page_data.replace('...', '')
    return page_data


def read_pages_from(pdfread, numPages):
    Book_data=''
    for i in range(0, numPages):
    	pageObj = pdfread.getPage(i)
	data_uni = pageObj.extractText()
        page_data = data_uni.encode('utf-8')
        page_data = strip_unicodes(page_data)
        if i == 0:
            page_data = page_data.replace('-', ' to ')
        yu = page_data.split(' ')
	if yu[0] in ['Index', '23.', 'Bibliography', 'Afterword', 'Introduction']:
	    continue
        else:
	    Book_data += page_data
    return Book_data

def get_Book_data(filepath):
    pdfread, book_len, pdfFileObj = convert_pdf_to_text(filepath)
    book_data = read_pages_from(pdfread, book_len)
    pdfFileObj.close()

    return book_data

def check_if_file_exists(filepath):
    if not os.path.exists(filepath):
        print("File path %s doesn't exists", filepath)
        sys.exit()
    fileext = filepath.split(".")[1]
    if fileext != "pdf":
        print("File %s is not PDF file", filepath)
        sys.exit()
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()                                               
    parser.add_argument("-f", "--file", type=str,
                        required=True, help="File path of pdf document")
    parser.add_argument("-o", "--outp", type=str,
                        required=True, help="name of output file")
    args = parser.parse_args()
    filepath = args.file
    if check_if_file_exists(filepath):
        book_data =  get_Book_data(filepath)
        myobj = gTTS(text=book_data, lang='en', slow=False)
        myobj.save(args.outp+".mp3")
        sys.exit()
