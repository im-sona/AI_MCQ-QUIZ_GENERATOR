In this project, building a web application using Flask, which allows users to upload documents (PDF, TXT, DOCX) and generate multiple-choice questions (MCQs) based on the content of the uploaded file. Here's a detailed breakdown of what we are doing:


![WhatsApp Image 2024-10-20 at 17 18 59_dd44d295](https://github.com/user-attachments/assets/0252bcde-1236-4fc9-951c-c100ef89bc12)

![WhatsApp Image 2024-10-20 at 16 38 36_8afb3a67](https://github.com/user-attachments/assets/4e3824d9-d9ee-4947-a379-947ea40be99e)
<img width="767" alt="image" src="https://github.com/user-attachments/assets/2f303730-bb63-4561-80c7-a84d90edbf8d">

![WhatsApp Image 2024-10-20 at 17 27 46_11017529](https://github.com/user-attachments/assets/201e714d-967f-4faf-91a6-0534e36557a4)

![WhatsApp Image 2024-10-20 at 17 25 53_56344f62](https://github.com/user-attachments/assets/80d87df8-2896-458c-925a-77317fb53388)

<img width="350" alt="image" src="https://github.com/user-attachments/assets/57e4a18a-e593-4cb2-b10f-3e59e4ea25ea">

![WhatsApp Image 2024-10-20 at 17 28 33_a225c9f1](https://github.com/user-attachments/assets/d7a23554-a215-4d89-a81c-38a9a27a2f46)
<img width="783" alt="image" src="https://github.com/user-attachments/assets/6fe2cc87-b422-400f-babd-6f1911fbf2e0">

1. File Upload Handling
Flask Web Application: Using Flask as the web framework to build the backend. <br>
File Upload: Users can upload a document (PDF, TXT, or DOCX). The file is processed on the server side after it is uploaded. <br>
File Type Check: In the allowed_file function, you check if the uploaded file has an extension of pdf, txt, or docx. This ensures that only valid file types are uploaded. <br>
2. Extracting Text from Uploaded Files <br>
Extracting Text: After the user uploads a file, you use the extract_text_from_file function to extract the text from the file. This function handles different file types:
PDF: You use the pdfplumber library to extract text from PDF files. <br>
DOCX: For DOCX files, you use the python-docx library to extract the text from the document.
TXT: For plain text files, you simply read the file and return its contents. <br>
Text Extraction Workflow: Once the file is uploaded, the extracted text is passed to the MCQ generator function.
3. Generating MCQs from the Extracted Text <br>
Generative AI: You are leveraging Google's Gemini AI model (via google.generativeai) to generate MCQs from the extracted text. This is done in the Question_mcqs_generator function. <br>
Prompt for AI: The AI is prompted to generate a set number of MCQs based on the text provided. The format of the MCQs is:
less <br>
## MCQ <br>
Question: [question] <br>
A) [option A] <br>
B) [option B] <br>
C) [option C] <br>
D) [option D] <br>
Correct Answer: [correct option]
Text-Based MCQ Generation: The AI model processes the text and generates a response that contains multiple MCQs, each with a clear question, four possible answers, and the correct answer. <br>
4. Saving the Generated MCQs <br>
Saving as TXT: After generating the MCQs, they are saved in a .txt file using the save_mcqs_to_file function. <br>
Saving as PDF: You use the create_pdf function to convert the MCQs into a PDF file using the FPDF library. This PDF is also saved in the RESULTS_FOLDER. <br>
5. Displaying the Generated MCQs <br>
Results Page: Once the MCQs are generated, the user is redirected to a results page (rendered via the results.html template) where they can view the MCQs in a well-formatted layout. <br>
MCQ Display: The MCQs are displayed on the webpage with options (A, B, C, D) and the correct answer hidden by default. Users can click a button to reveal the correct answer.
Download Links: The user is also given the option to download the generated MCQs in both TXT and PDF formats.
6. User Interface <br>
Upload Form: The index.html template provides a simple form where users can upload their document and specify the number of MCQs they want. <br>
Responsive Design: The frontend is designed to be responsive, so it looks good on both desktop and mobile devices. <br>
Styling: You are using custom CSS in both the index.html and results.html templates to ensure the user interface is clean and visually appealing. <br>
7. Flask Routes and API Endpoints <br>
Route /: This is the home page, where the user can upload the file and specify how many questions they want to generate.
Route /generate: This route handles the file upload and MCQ generation process. It is responsible for extracting text, generating MCQs, and displaying the results.
Route /download/<filename>: This route allows users to download the generated MCQ files (both TXT and PDF). <br>
8. Additional Features <br>
Answer Toggle: In the results.html template, you provide a "Click to view answer" button that allows the user to toggle the visibility of the correct answers for each MCQ. <br>
File Management: The uploaded files are saved in the UPLOAD_FOLDER, and the generated results (TXT and PDF files) are saved in the RESULTS_FOLDER. These files are then made available for the user to download. <br>
Flow Summary: <br>
User uploads a file (PDF, DOCX, or TXT) through the form on the homepage. <br>
Text is extracted from the file using different libraries based on the file type. <br>
The AI model generates the requested number of MCQs based on the extracted text. <br>
The generated MCQs are saved in both TXT and PDF formats. <br>
The MCQs are displayed to the user on a results page, with the ability to toggle the visibility of the correct answer. <br>
The user can download the MCQs in TXT or PDF format.
Tech Stack: <br>
Backend: Flask (Python) <br>
AI: Google Generative AI (Gemini Model) <br>
File Handling: pdfplumber, python-docx, FPDF <br>
Frontend: HTML, CSS (Responsive Design) <br>
Deployment: Local development (Flask server) <br>
This project combines file processing, natural language processing (using an AI model), and dynamic web development to generate MCQs automatically from various text formats.
