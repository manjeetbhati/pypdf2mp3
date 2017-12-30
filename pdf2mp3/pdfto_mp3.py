# Import the required module for text 
# to speech conversion
import PyPDF2
from gtts import gTTS
import os
import re
 
def convert_pdf_to_text():
    pdfFileObj = open('peopleus.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    numPages = pdfReader.numPages
    return pdfReader,numPages,pdfFileObj

def strip_unicodes(book_data):
    book_data.replace('\xe2', '')
    book_data.replace('\xe2', '')
    book_data.replace('\x84', '')
    book_data.replace('\xa2', '')
    return book_data


def fread_pages_from(pdfread, numPages):
    Book_data=''
    pageObj = pdfread.getPage(186)
    data_uni = pageObj.extractText()
    page_data = data_uni.encode('utf-8')
    page_data = page_data.replace('\xe2', '')
    page_data = page_data.replace('\xe2', '')
    page_data = page_data.replace('\x84', '')
    page_data = page_data.replace('\xa2', '')
    myobj = gTTS(text=page_data, lang=language, slow=False)
    myobj.save("book187.mp3")
    Book_data += page_data

def read_pages_from(pdfread, numPages):
    Book_data=''
    for i in range(0, numPages):
    	pageObj = pdfread.getPage(i)
	data_uni = pageObj.extractText()
	page_data = data_uni.encode('utf-8')
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
        if i == 0:
            page_data = page_data.replace('-', ' to ')
        yu = page_data.split(' ')
	if yu[0] in ['Index', '23.', 'Bibliography', 'Afterword', 'Introduction']:
	    continue
        else:
	    Book_data += page_data
    return Book_data

def get_Book_data():
    pdfread, book_len, pdfFileObj = convert_pdf_to_text()
    book_data = read_pages_from(pdfread, book_len)
    pdfFileObj.close()

    return book_data

language = 'en'

book_data =  get_Book_data()
myobj = gTTS(text=book_data, lang=language, slow=False)
myobj.save("book.mp3")
