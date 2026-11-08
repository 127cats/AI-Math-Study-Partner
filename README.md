# ✨ AI Math Study Partner

An interactive desktop application built with Python and Tkinter to help students practice and master mathematics using AI. 

## 🚀 Key Features
- **Smart Q&A (Text & Image):** Ask math questions using text or upload images of problems. The AI (Zhipu GLM-4v) reads the image and provides step-by-step plain-text solutions.
- **Mistake Tracker:** Automatically saves tricky questions to a local SQLite database so you can review them anytime.
- **AI Reform Practice:** Generates variations of your past mistakes for endless practice.
- **Note Management:** Keep all your math formulas and notes organized in one place.
- **History Log:** View all your past questions and AI answers.

## 🛠️ Tech Stack
- **Language:** Python 3.12
- **GUI:** Tkinter
- **Database:** SQLite3
- **AI Integration:** [Zhipu AI API](https://bigmodel.cn/apikey/platform) (`glm-4-flash` & `glm-4v-flash` for vision)
  - **Notes 📝:** New users receive a complimentary 20,000,000 token trial package (requires registration with a phone number).
- **Image Processing:** Pillow (PIL)

## ⚙️ How to Run
1. Clone this repository to your local machine.
2. Install the required Python packages:
   ```bash
   pip install zhipuai pillow
   
3. Open Github_ai_api.py and insert your Zhipu API Key:
   ```bash
   API_KEY = "YOUR_ZHIPU_API_KEY_HERE"
4. Run the main application in your terminal:
   ```bash
   python3 Github_Math_Practice.py

## 🧠 About the Code
This project was built with a focus on modularity and readability:
- The UI logic and database connections are handled in Github_Math_Practice.py.
- The AI API calls and image base64 encoding are separated into Github_ai_api.py.
- It uses os.path to dynamically locate the SQLite database, ensuring it runs perfectly on any machine.

## 👨‍💻 Author's Note
This project was initially created as my final Grade 10 Computer Science school project... 
However, I decided to dive deeper into this, which I realized the potential of this tool! I chose to go beyond the basic requirements adding image recognition, refining the UI, and structuring the code properly.
This journey taught me how to integrate real world AI APIs, manage local databases, and debug complex UI interactions. I hope this little app can help other students who struggle with math just like I do! ✨

If you like this project, feel free to give it a ⭐!


