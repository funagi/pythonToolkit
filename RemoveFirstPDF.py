import os,sys
from pyPdf import PdfFileWriter, PdfFileReader
from utils import printc

if len(sys.argv)==1:
    printc("Drop files on me to process...",'red')
    raw_input('\nPress any key to exit...')
else:
    try:
        lst = sys.argv[1:]
        count = len(lst)
        length = len(str(count))
        #print lst
        for item in lst:
            pdf_in = PdfFileReader(file(item, 'rb'))
            pdf_out = PdfFileWriter()
            file_out = file(item.replace('.pdf','.new.pdf'), 'wb')
            for x in xrange(1, pdf_in.getNumPages()):
                pdf_out.addPage(pdf_in.getPage(x))
            pdf_out.write(file_out)
            file_out.close()

            pos = item.rindex('.')+1
            name = item[:pos]
            sname = item[item.rindex('\\')+1:pos-1]
            
            printc(('[%' + str(length) +'d/%' + str(length) + 'd] ') % (lst.index(item)+1,count), 'green', end='')
            print sname+'.new.pdf'
    except Exception as e:
        printc(e.message,'red')

    finally:
        raw_input('\nPress any key to exit...')

