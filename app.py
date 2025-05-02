import os
from flask import Flask, render_template, request, send_file
import pdfplumber
import docx
from werkzeug.utils import secure_filename
import google.generativeai as genai
from fpdf import FPDF  

# Set your API key
os.environ["GOOGLE_API_KEY"] = "AAIzaSyAUz4YTseHi9ob_H3OBm7xq-wX9NaYr6SQ"  
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULTS_FOLDER'] = 'results/'
app.config['QUIZ_FOLDER'] = 'quiz_results/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt', 'docx'}

# Ensure necessary folders exist
for folder in [app.config['UPLOAD_FOLDER'], app.config['RESULTS_FOLDER'], app.config['QUIZ_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_file(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            text = ''.join([page.extract_text() for page in pdf.pages if page.extract_text()])
        return text
    elif ext == 'docx':
        doc = docx.Document(file_path)
        return ' '.join([para.text for para in doc.paragraphs])
    elif ext == 'txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    return None

def generate_mcqs(input_text, num_questions, language):
    prompt = f"""
    You are an AI assistant helping generate multiple-choice questions (MCQs) based on the following text.
    The text is in {language}.
    '{input_text}'
    Please generate {num_questions} MCQs. Each question should have:
    - A clear question
    - Four answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    Format:
    ## MCQ
    Question: [question]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]

    Correct Answer: [correct option]
    

    Explanation: [1-5 line explanation ]

    """
    response = model.generate_content(prompt).text.strip()
    return response

def remove_answers(mcqs):
    """Creates a version of the MCQs without answers for the quiz page."""
    quiz_mcqs = []
    for mcq in mcqs.split("## MCQ"):
        if mcq.strip():
            quiz_mcq = mcq.split("Correct Answer:")[0].strip()
            quiz_mcqs.append("## MCQ\n" + quiz_mcq)
    return "\n".join(quiz_mcqs)

def save_file(content, filename, folder):
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return file_path

def save_correct_answers(mcqs, filename, folder):
    """Extract correct answers from MCQs and save them separately."""
    answers_path = os.path.join(folder, filename)
    with open(answers_path, 'w', encoding='utf-8') as f:
        for mcq in mcqs.split("## MCQ"):
            if mcq.strip():
                lines = mcq.strip().split("\n")
                for line in lines:
                    if line.startswith("Correct Answer:"):
                        correct_answer = line.split(":")[-1].strip()
                        f.write(correct_answer + "\n")
    return answers_path

def create_pdf(mcqs, filename, folder):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for mcq in mcqs.split("## MCQ"):
        if mcq.strip():
            pdf.multi_cell(0, 10, mcq.strip())
            pdf.ln(5)

    pdf_path = os.path.join(folder, filename)
    pdf.output(pdf_path)
    return pdf_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    language = request.form['language']
    num_questions = int(request.form['num_questions'])

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        text = extract_text_from_file(file_path)
        if not text:
            return "Could not extract text from file"

        mcqs = generate_mcqs(text, num_questions, language)

        txt_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.txt"
        pdf_filename = f"generated_mcqs_{filename.rsplit('.', 1)[0]}.pdf"
        save_file(mcqs, txt_filename, app.config['RESULTS_FOLDER'])
        create_pdf(mcqs, pdf_filename, app.config['RESULTS_FOLDER'])

        quiz_txt_filename = f"quiz_mcqs_{filename.rsplit('.', 1)[0]}.txt"
        quiz_pdf_filename = f"quiz_mcqs_{filename.rsplit('.', 1)[0]}.pdf"
        quiz_mcqs = remove_answers(mcqs)
        save_file(quiz_mcqs, quiz_txt_filename, app.config['QUIZ_FOLDER'])
        create_pdf(quiz_mcqs, quiz_pdf_filename, app.config['QUIZ_FOLDER'])

        answer_filename = f"answers_{filename.rsplit('.', 1)[0]}.txt"
        save_correct_answers(mcqs, answer_filename, app.config['QUIZ_FOLDER'])

        return render_template('generate_mcq.html', mcqs=mcqs)
@app.route('/take_quiz', methods=['GET', 'POST'])
def take_quiz():
    quiz_files = [f for f in os.listdir(app.config['QUIZ_FOLDER']) if f.endswith('.txt')]

    if not quiz_files:
        return "No quizzes available. Please generate MCQs first."

    latest_quiz_file = os.path.join(app.config['QUIZ_FOLDER'], quiz_files[-1])

    with open(latest_quiz_file, 'r', encoding='utf-8') as file:
        quiz_mcqs = file.read()

    # Dictionary to store correct answers from the file for comparison
    correct_answers = {}
    for mcq in quiz_mcqs.split('## MCQ'):
        if mcq.strip():
            question = mcq.split('A)')[0].strip()
            
            # Check if 'Correct Answer:' is in the MCQ text
            if 'Correct Answer:' in mcq:
                correct_answer = mcq.split('Correct Answer:')[1].strip()
            else:
                correct_answer = None  # If no correct answer, set to None

            correct_answers[question] = correct_answer

    if request.method == 'POST':
        user_answers = {f"question_{i+1}": request.form.get(f"question_{i+1}") for i in range(len(correct_answers))}
        
        # Calculate score
        score = 0
        correct_count = 0
        incorrect_count = 0
        
        for i, (question, correct_answer) in enumerate(correct_answers.items()):
            user_answer = user_answers.get(f"question_{i+1}")
            if user_answer == correct_answer:
                score += 1
                correct_count += 1
            else:
                incorrect_count += 1

        total_questions = len(correct_answers)
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0

        # Pass results to the submit page including percentage
        return render_template(
            'submit.html',
            score=score,
            correct_count=correct_count,
            incorrect_count=incorrect_count,
            total_questions=total_questions,
            percentage=percentage
        )

    return render_template('take_quiz.html', mcqs=quiz_mcqs)











if __name__ == "__main__":
    app.run(debug=True)
