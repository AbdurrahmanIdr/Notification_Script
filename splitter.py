import os
from PyPDF2 import PdfReader, PdfWriter

def pdf_splitter(filename):
    """
    Accept a pdf file name and splits it into pages
    with *.pdf extension 
    
    filename: str
    
    returns
    
    
    """
    
    filer = filename.split('.')[0]
    if not os.path.exists(filer): os.mkdir(filer)    
    
    if filename.endswith('.pdf'):
        pdf_file = PdfReader(filename)
        page_nums = len(pdf_file.pages)
        
        for i in range(page_nums):
            file_writer = PdfWriter()
            file_writer.merge(position=i, fileobj=pdf_file, pages=[i])
            file_writer.write(f'{filer}/page{i}.pdf')
            print(f'{filer}/file{i}.pdf written succesfully')
            
    return True
            
    print('Not a PDF file')
    return False



def contents_extractor(filename):
    """"
    Extracts the needed contents from the pdf file
    
    args:
    filename : str
    
    return
    
    """
    
    if filename.endswith('.pdf'): 
        
        file_cont = PdfReader(filename)
        
        contents = file_cont.pages[0].extract_text().split('\n')

        conts2 = contents[3:6]

        dates = conts2[0].strip().split('-')
        d_mon = dates[0]
        d_year = dates[-1]
        sur_name = conts2[1].split(':')[1].split(',')[0].strip()
        ippis = conts2[-1].split(':')[-1].strip()
        
        new_name = f'{ippis}_{sur_name}_{d_mon}_{d_year}.pdf'

        
        os.rename(filename, new_name)
        print(f'renamed {filename} to {new_name}')
        

def split_rename(filename):
    splitter = pdf_splitter(filename)
    foldername = filename.split('.')[0]
    if splitter:
        files = os.listdir(foldername)
        for file in files:
            contents_extractor(file)
            print('done')
        
    
