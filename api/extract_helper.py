# from pathlib import Path
# import tempfile
# import requests
# from pathlib import Path
# import pprint
# from science_parse_api.api import parse_pdf
# from science_parse_api.test_helper import test_data_dir
# import fitz # install using: pip install PyMuPDF

# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# import io

# def pdf_to_text(input_file,output):
#     i_f = open(input_file,'rb')
#     resMgr = PDFResourceManager()
#     retData = io.StringIO()

#     TxtConverter = TextConverter(resMgr,retData, laparams= LAParams())
#     interpreter = PDFPageInterpreter(resMgr,TxtConverter)
#     for page in PDFPage.get_pages(i_f):
#         interpreter.process_page(page)

#     txt = retData.getvalue()
    
#     #lowercase should not be done here
#     txt = txt.lower()
#     #split txt when the word introduction appears
#     intro_start = txt.split('introduction')[1]

#     #take txt until references
#     intro_no_references = intro_start.split('references')[0]

#     source_text = ''
#     final_source_text = ''
#     #replace all '\n' with ' '
#     for line in intro_no_references.split('\n'):
#         source_text += line + ' '

#     #loop through every line in intro_no_references
#     for sentence in source_text.split('.'):
#         if len(sentence) <= 10:
#             continue
#         final_source_text += sentence + '\n'

#     print(source_text)

    
#     # with open(output,'w') as of:
#     #     of.write(bytes(txt, 'utf-8').decode('utf-8', 'ignore'))

# input_pdf = '2206_00073.pdf'
# output_txt = 'sample.txt'
# pdf_to_text(input_pdf,output_txt)

    

# def extract_pdf():
#     try:
#         # Tries to find the folder `test_data`
#         PDFDirectory = './PDF/'
#         pdf_paper = Path(PDFDirectory + '2206.00073.pdf')
        
#         host = 'http://127.0.0.1'
#         port = '80'
#         output_dict = parse_pdf(host, pdf_paper, port=port)

#         pp = pprint.PrettyPrinter(indent=4)
#         pp.pprint(output_dict)

#     except FileNotFoundError:
#         print('File not found')

# def extract_pdf():

#     try:
#         # Tries to find the folder `test_data`
#         test_data_directory = test_data_dir()
#         test_pdf_paper = Path(test_data_directory, 
#                         'example_for_test.pdf').resolve()

#         host = 'http://127.0.0.1'
#         port = '8080'
#         output_dict = parse_pdf(host, test_pdf_paper, port=port)

#         pp = pprint.PrettyPrinter(indent=4)
#         pp.pprint(output_dict)

#     except FileNotFoundError:
#         # If it cannot find that folder will get the pdf and 
#         # image from Github. This will occur if you are using 
#         # Google Colab
#         pdf_url = ('https://github.com/UCREL/science_parse_py_api/'
#                 'raw/master/test_data/example_for_test.pdf')
#         temp_test_pdf_paper = tempfile.NamedTemporaryFile('rb+')
#         test_pdf_paper = Path(temp_test_pdf_paper.name)
#         with test_pdf_paper.open('rb+') as test_fp:
#             test_fp.write(requests.get(pdf_url).content)

#         image_url = ('https://github.com/UCREL/science_parse_py_api'
#                     '/raw/master/test_data/example_test_pdf_as_png.png')
#         image_file = tempfile.NamedTemporaryFile('rb+', suffix='.png')
#         with Path(image_file.name).open('rb+') as image_fp:
#             image_fp.write(requests.get(image_url).content)


