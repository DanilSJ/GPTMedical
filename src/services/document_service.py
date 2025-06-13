import os
from typing import Optional
from docx import Document
from PyPDF2 import PdfReader
import io
import magic
from PIL import Image
import pytesseract

class DocumentService:
    @staticmethod
    async def extract_text_from_document(file_data: bytes, filename: str) -> Optional[str]:
        """
        Извлекает текст из документа различных форматов
        """
        # Определяем тип файла по расширению
        file_extension = os.path.splitext(filename)[1].lower()
        print(f"Processing file: {filename}, extension: {file_extension}")
        
        try:
            # Определяем MIME-тип файла
            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(file_data)
            print(f"File MIME type: {file_type}")
            
            if file_type == 'application/pdf':
                print("Processing as PDF")
                return DocumentService._extract_from_pdf(file_data)
            elif file_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
                print("Processing as DOCX/DOC")
                return DocumentService._extract_from_docx(file_data)
            elif file_type.startswith('image/'):
                print(f"Processing as image: {file_type}")
                return DocumentService._extract_from_image(file_data)
            else:
                print(f"Unsupported file type: {file_type}")
                return None
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            return None

    @staticmethod
    def _extract_from_pdf(file_data: bytes) -> str:
        """
        Извлекает текст из PDF файла
        """
        try:
            pdf_file = io.BytesIO(file_data)
            pdf_reader = PdfReader(pdf_file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
                
            return text.strip()
        except Exception as e:
            print(f"Error extracting from PDF: {str(e)}")
            raise

    @staticmethod
    def _extract_from_docx(file_data: bytes) -> str:
        """
        Извлекает текст из DOCX файла
        """
        try:
            docx_file = io.BytesIO(file_data)
            doc = Document(docx_file)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
                
            return text.strip()
        except Exception as e:
            print(f"Error extracting from DOCX: {str(e)}")
            raise

    @staticmethod
    def _extract_from_image(file_data: bytes) -> str:
        """
        Извлекает текст из изображения с помощью OCR
        """
        try:
            # Открываем изображение из байтов
            image = Image.open(io.BytesIO(file_data))
            
            # Извлекаем текст с помощью Tesseract OCR
            text = pytesseract.image_to_string(image, lang='rus+eng')
            
            return text.strip()
        except Exception as e:
            print(f"Error extracting from image: {str(e)}")
            raise 