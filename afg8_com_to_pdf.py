import os.path

import comtypes.client

word = comtypes.client.CreateObject('Word.Application')

in_file = os.path.abspath(os.path.join('.', 'documents/dummy1.docx'))
out_file = os.path.abspath(os.path.join('.', 'documents/dummy1.pdf'))

document = word.documents.Open(in_file)
document.SaveAs(out_file, FileFormat=17)

document.Close()
