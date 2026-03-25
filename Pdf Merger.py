from pypdf import PdfWriter
import os
def pdfMerger(file1,file2,output):
    if not os.path.exists(file1):
        print(f"Error:'{file1}' is not exist")
        return
    if not os.path.exists(file2):
        print(f"Error:'{file2}' is not exist")
        return
    merger = PdfWriter()
    merger.append(file1)
    merger.append(file2)
    merger.write(output)
    print(f"PDFs merged successfully '{output}'")
pdfMerger("D:/pythonpracticeagainVS/IT-1.pdf","D:/pythonpracticeagainVS/IT-1.pdf","D:/pythonpracticeagainVS/combined.pdf")
print("Thank You User")