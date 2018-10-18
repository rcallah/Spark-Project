'''
########################
# general pdf miner code check
# uses:#details on this part: http://www.unixuser.org/~euske/python/pdfminer/programming.html#basic
########################
'''
import pdfminer
import json
import sys
import urllib
import logging 
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import os

class pdf2text:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler('logginginfo.log')
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.INPUT_DIRECTORY='pdf_cases_input'
        self.OUTPUT_DIRECTORY='pdf_cases_output'

    '''
    ########################
    VERSION
    ########################
    '''
    def convert_pdf_to_text(self, path, INPUT_DIRECTORY,OUTPUT_DIRECTORY ):
        ##details on this part: http://www.unixuser.org/~euske/python/pdfminer/programming.html#basic
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        #set the code
        codecx = 'utf-8'
        # Set parameters for analysis.
        laparams = LAParams()
        # Create a PDF page aggregator object.
        device = TextConverter(rsrcmgr, retstr, codec=codecx, laparams=laparams)
        #read the file
        fp = file(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()
    
        for page in PDFPage.get_pages(fp, pagenos,
                                      maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):    
            interpreter.process_page(page)
    
        text = retstr.getvalue()
            
    
        fp.close()
        device.close()
        retstr.close()
        filename =  os.path.basename(path)
        # xml data
        os.system("dumppdf.py -a "+ path + " >> "+ OUTPUT_DIRECTORY+ "/"+"OUTPUT_"+filename+".xml")
     
        #file
        with open(OUTPUT_DIRECTORY+ "/"+ "OUTPUT_"+filename+".txt", 'w') as write_file:
            write_file.write(text)
        
 

    '''
    ########################
    check if the input folder file is processed or not
    ########################
    '''
    def checknotPROCESSED(self, infilename,folder): 
        for afile in os.listdir(folder):
                if afile==infilename+".txt":
                    return True
        return False


def main():
    print "PROCESSING....."
    obj= pdf2text()
    for infile in os.listdir(obj.INPUT_DIRECTORY+"/"):
        if infile.endswith(".pdf"):
            if not obj.checknotPROCESSED("OUTPUT_"+infile,obj.OUTPUT_DIRECTORY):
                print("[New File]:"+infile)
                text2read = obj.convert_pdf_to_text(obj.INPUT_DIRECTORY+"/"+infile)
                print text2read
            else:
                obj.logger.info("FILE:["+ infile+ "]already processed")
                print("FILE:["+ infile+ "]already processed")
    print "END..."

if  __name__ =='__main__':main()            







