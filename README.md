
# 💡 Smart AI MCQ and Quiz Generator

A powerful web application that uses **AI (Gemini API)** to generate multiple-choice questions (MCQs) from uploaded documents (PDF, DOCX, or TXT) and allows users to take interactive quizzes — perfect for students, educators, and trainers!

## 🚀 Features

- 📄 Upload PDF, DOCX, or text files
- 🧠 Automatically generate MCQs using **Gemini API**
- 🌐 Select quiz language (English or others)
- ✅ Display correct answers with explanations
- 📝 Take quizzes in a user-friendly format
- 📊 View score and performance chart

## 🔧 Tech Stack

| Frontend | Backend  | AI Integration |
|----------|----------|----------------|
| HTML5    | Python   | Gemini API     |
| CSS3     | Flask    |                |
| Bootstrap|          |                |

## 📸 Screenshots

### 📤 Upload Document and Generate MCQs
<img width="1920" height="1020" alt="Take Quiz - Google Chrome 2_9_2025 3_08_26 PM" src="https://github.com/user-attachments/assets/7548ea27-1eda-403d-af1b-c3550a5705e6" />


### 📄 Generated MCQs with Answers
<img width="1920" height="1020" alt="Generated MCQs - Google Chrome 2_9_2025 3_10_43 PM" src="https://github.com/user-attachments/assets/6c80dd7b-3183-4f36-8034-74160cf0ddbd" />


### 🧪 Take Quiz Interface
<img width="1920" height="1020" alt="Generated MCQs - Google Chrome 2_9_2025 3_11_12 PM" src="https://github.com/user-attachments/assets/dd8c7b86-5bc0-466d-8ecd-b951a02a4734" />

### 📈 Quiz Results
<img width="1920" height="1020" alt="Quiz Results and 2 more pages - Personal - Microsoft​ Edge 4_22_2025 10_05_37 PM" src="https://github.com/user-attachments/assets/2eeb5214-4b2d-4304-a37f-896c2770fefa" />

## 🛠️ How It Works

1. **Upload** a document (PDF, DOCX, or text)
2. Choose the number of pages and language
3. Click **"Generate MCQs"**
4. View or **Take the Quiz**
5. Submit answers and get instant **score + feedback**

## 📁 Project Structure

```
smart_ai_mcq_generator/
│
├── static/                 # CSS, Bootstrap files
├── templates/              # HTML Templates (upload, quiz, result)
├── app.py                  # Flask backend
├── mcq_generator.py        # MCQ creation using Gemini API
├── requirements.txt
└── README.md
```

## ✅ Setup Instructions

1. **Clone the repo**:
   ```bash
   git clone https://github.com/your-username/smart-ai-mcq-generator.git
   cd smart-ai-mcq-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Gemini API key**:
   - Add your key in `.env` or directly in the Python file (if securely handled).

4. **Run the Flask app**:
   ```bash
   python app.py
   ```

5. Open in browser: `http://127.0.0.1:5000`

## 🔮 Future Enhancements

- Export MCQs to PDF
- User login & score history
- Multi-language support
- Timer-based quiz

## 🧑‍💻 Author

Developed by **[Sona IM]**
