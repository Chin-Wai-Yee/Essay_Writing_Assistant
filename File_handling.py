from PIL import Image
import docx2txt
import PyPDF2

def read_file_content(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1]
    
    if file_type in ['jpg', 'jpeg', 'png']:
        return Image.open(uploaded_file), file_type
    
    elif file_type == 'txt':
        return uploaded_file.getvalue().decode('utf-8'), file_type
    
    elif file_type in ['doc', 'docx']:
        return docx2txt.process(uploaded_file), file_type
    
    elif file_type == 'pdf':
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text, file_type
    
    else:
        return "Unsupported file type", "unsupported"