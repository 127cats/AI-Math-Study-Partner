import os
import random
from tkinter import filedialog
from PIL import Image, ImageTk 
from Github_ai_api import ask_math #Here you implement ask_math function from ai_api.py file
import tkinter as tk
from tkinter import ttk
import sqlite3
import time
last_question = ""
last_answer = ""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "Database_training.db") #This connects to your database file
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()


window = tk.Tk()
window.geometry("800x800")
window.title('✨ AI Math Study Partner ✨')

option = [
    "Training Mode",
    "Note Management",
    "Mistake Tracker",
    "History",
]



clicked = ttk.Combobox(window, values=option, state="readonly")
clicked.pack(pady=18)
clicked.set("Training Mode") 

page_training = tk.Frame(window)
page_notes = tk.Frame(window)
page_mistake = tk.Frame(window)
page_history = tk.Frame(window)
page_ai_qa = tk.Frame(window)
page_ai_reform = tk.Frame(window)

page_training.configure(bg="lightblue")
page_notes.configure(bg="lightgreen")
page_mistake.configure(bg="lightcoral")
page_history.configure(bg="lightyellow")
page_ai_reform.configure(bg="lightblue")
page_ai_qa.configure(bg="lightblue")



# ========== Traning Mode ==========
def switch_page():
    selected = clicked.get()
    
    page_training.pack_forget()
    page_notes.pack_forget()
    page_mistake.pack_forget()
    page_history.pack_forget()
    page_ai_qa.pack_forget()
    page_ai_reform.pack_forget()
    


    if selected == "Training Mode":
        page_training.pack(fill="both", expand=True)
    elif selected == "Note Management":
        page_notes.pack(fill="both", expand=True)
    elif selected == "Mistake Tracker":
        page_mistake.pack(fill="both", expand=True)
    elif selected == "History":
        page_history.pack(fill="both", expand=True)


def go_to_qa():
    page_training.pack_forget()
    page_ai_qa.pack(fill="both", expand=True)

def go_to_reform():
    page_training.pack_forget()
    page_ai_reform.pack(fill="both", expand=True)

def back_to_training():
    page_ai_qa.pack_forget()
    page_ai_reform.pack_forget()
    page_training.pack(fill="both", expand=True)


tk.Label(page_training, text="Training Mode", font=("Helvetica", 24, "bold"), bg="lightblue", fg = "#333333").pack(pady=(10,0))

btn_qa = tk.Button(page_training, text="AI Smart Q&A", command=go_to_qa, fg="Black")
btn_qa.pack(pady=10)

btn_reform = tk.Button(page_training, text="AI Reform Practice", command=go_to_reform, fg="Black")
btn_reform.pack(pady=5)

def clear_qa():
    global selected_image_path
    question_entry.delete(0, tk.END)  
    answer_text.delete("1.0", tk.END) 
    selected_image_path = None        
    image_preview.config(image="")    
    image_preview.image = None



# ========== Smart Q&A ==========
tk.Label(page_ai_qa, text="Smart Q&A", font=("Helvetica", 24, "bold"), bg="lightblue", fg="#333333").pack(pady=(20, 10))
back_btn_qa = tk.Button(page_ai_qa, text="← Back", command=back_to_training)
back_btn_qa.pack(pady=10)

clear_btn = tk.Button(page_ai_qa, text="🗑️ Clear", font = ("Arial", 14, "bold"), command=clear_qa, fg="#333333")
clear_btn.pack(side="bottom", pady=20)


tk.Label(page_ai_qa, text="Enter your questions:", bg="lightblue", fg="#333333").pack()

input_frame = tk.Frame(page_ai_qa, bg="lightblue")
input_frame.pack(pady=5)

question_entry = tk.Entry(input_frame, width=40)
question_entry.pack(side="left", padx=5)

global selected_image_path
selected_image_path = None  

def upload_image():
    global selected_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        selected_image_path = file_path
        img = Image.open(file_path)
        img.thumbnail((200, 200)) 
        photo = ImageTk.PhotoImage(img)
        image_preview.config(image=photo)
        image_preview.image = photo 

upload_btn = tk.Button(input_frame, text="📷 Upload", command=upload_image, bg="#2196F3", fg="#333333")
upload_btn.pack(side="left", padx=5)

image_preview = tk.Label(page_ai_qa, bg="lightblue")
image_preview.pack()


def ask_question():
    global last_question, last_answer, selected_image_path
    question = question_entry.get().strip()
    
    print(f"--- DEBUG Q&A ---")
    print(f"Question: {question}")
    print(f"Image Path: {selected_image_path}") 
    
    if question or selected_image_path:
        answer_text.delete("1.0", tk.END)
        answer_text.insert("1.0", "🤔 AI is thinking...")
        window.update()
        
        ai_answer = ask_math(question, selected_image_path)
        
        answer_text.delete("1.0", tk.END)
        answer_text.insert("1.0", f"【AI Answer】\n\n{ai_answer}")
        
        if selected_image_path:
            last_question = f"{question}\n[Image: {selected_image_path}]"
        else:
            last_question = question
            
        last_answer = ai_answer
    else:
        answer_text.delete("1.0", tk.END)
        answer_text.insert("1.0", "Please enter a question or upload an image!")


def save_to_mistake(function_ai = "Smart Q&A"):
    global last_question, last_answer
    
    if not last_question:
        answer_text.insert(tk.END, "\n\n✗ No question to save. Please ask a question first!")
        return
    
    current_time = time.time()
    
    cursor.execute('''
        INSERT INTO "training" (Question, Answer, create_at, Function)
        VALUES (?,?,?,?)
    ''', (last_question, last_answer, current_time, function_ai))

    cursor.execute('''
        INSERT INTO History (All_Question, All_Answer, overall_time)
        VALUES (?, ?, ?)
    ''', (last_question, last_answer, current_time))

    connection.commit()
    
    answer_text.insert(tk.END, f"\n\n✓ Question saved to Mistake Tracker！")

ask_btn = tk.Button(page_ai_qa, text="Q&A", command=ask_question)
ask_btn.pack(pady=5)

tk.Label(page_ai_qa, text="AI Answer：", bg="lightblue", fg = "#333333").pack()
answer_text = tk.Text(page_ai_qa, height=20, width=70, font=("Courier", 12))
answer_text.pack(pady=5)


save_btn = tk.Button(page_ai_qa, text="Saved to Mistake Tracker", command=save_to_mistake, bg="#F56E38", fg="Black")
save_btn.pack(pady=5)



# ===== AI Reform）=====
tk.Label(page_ai_reform, text="Practice from Your Mistakes", font=("Helvetica", 24, "bold"), bg="lightblue", fg = "#333333").pack(pady=(10,0))

back_btn = tk.Button(page_ai_reform, text="← Back", command=back_to_training)
back_btn.pack(pady=5)

question_display = tk.Text(page_ai_reform, height=6, width=70)
question_display.pack(pady=10)

tk.Label(page_ai_reform, text="Your answer:", bg="lightblue", fg = "#333333").pack()
user_answer_entry = tk.Entry(page_ai_reform, width=50)
user_answer_entry.pack(pady=5)

current_q = ""
current_a = ""

import re  

def get_random_question():
    """从数据库随机拿一道错题，并稍微修改数字实现 Reform"""
    cursor.execute('SELECT Question, Answer FROM "training" ORDER BY RANDOM() LIMIT 1')
    row = cursor.fetchone()
    
    if not row:
        return None, None
    
    original_q, original_a = row
    
    def change_number(match):
        num = int(match.group())
        return str(num + random.choice([-1, 1]))  # 随机加1或减1
        
    new_q = re.sub(r'\d+', change_number, original_q)
    
    match = re.search(r'(?:Final answer:|answer:|answer is|=)\s*(-?\d+(?:\.\d+)?)', original_a, re.IGNORECASE)
    if match:
        pure_answer = match.group(1)  
    else:
        pure_answer = original_a.strip() 
        
    return new_q, pure_answer

def new_question():
    global current_q, current_a
    current_q, current_a = get_random_question()
    
    if not current_q:
        question_display.delete("1.0", tk.END)
        question_display.insert("1.0", "No mistakes yet! Go practice first.")
        return
    
    question_display.delete("1.0", tk.END)
    question_display.insert("1.0", f"📝 {current_q}")
    user_answer_entry.delete(0, tk.END)

def check_answer():
    global current_a  
    
    user_ans = user_answer_entry.get().strip()
    if not user_ans:
        question_display.insert(tk.END, "\n\n⚠️ Please enter your answer!")
        return
    
    question_display.insert(tk.END, "\n\n🤔 AI is checking your answer...")
    window.update()
    
    prompt = f"Question: {current_q}\nStudent's answer: {user_ans}\nIs the student correct? Provide the correct answer in the format 'Correct answer: [number]', then Please answer 'Correct✅' or 'Wrong❌'"
    ai_result = ask_math(prompt)
    
    question_display.insert(tk.END, f"\n\n🤖 AI Result:\n{ai_result}")
    
    import re
    match = re.search(r'Correct answer:\s*(-?\d+(?:\.\d+)?)', ai_result, re.IGNORECASE)
    if match:
        current_a = match.group(1)



tk.Button(page_ai_reform, text="New Question", command=new_question, fg="black").pack(pady=5)
tk.Button(page_ai_reform, text="Check Answer", command=check_answer, fg="black").pack(pady=5)


def save_reform_to_mistake():
    global current_q, current_a
    
    if not current_q:
        question_display.insert(tk.END, "\n\n✗ No question to save. Click 'New Question' first!")
        return
        
    if not current_a:
        question_display.insert(tk.END, "\n\n✗ No answer available!")
        return
    
    current_time = time.time()
    
    cursor.execute('''
        INSERT INTO "training" (Question, Answer, create_at, Function)
        VALUES (?, ?, ?, ?)
    ''', (current_q, current_a, current_time, "AI Reform"))
    
 
    cursor.execute('''
        INSERT INTO History (All_Question, All_Answer, overall_time)
        VALUES (?, ?, ?)
    ''', (current_q, current_a, current_time))
    
    connection.commit()

    question_display.insert(tk.END, "\n\n✓ Question saved to Mistake Tracker!")


save_btn_2 = tk.Button(page_ai_reform, text="Saved to Mistake Tracker", command=save_reform_to_mistake, bg="#F56E38", fg="Black")
save_btn_2.pack(pady=5)

new_question()



# ========= Note Book Section ===========
tk.Label(page_notes, text="Note Management", font=("Helvetica", 24, "bold"), bg= "lightgreen", fg = "#333333").pack(pady=(10,0))

tk.Label(page_notes, text="Title:", bg="lightgreen", fg = "black").pack()
title_entry = tk.Entry(page_notes, width=50)
title_entry.pack(pady=5)

tk.Label(page_notes, text="Add your Notes:", bg="lightgreen", fg = "black").pack()
content_entry = tk.Text(page_notes, height=8, width=60)
content_entry.pack(pady=5)

def submit_note():
    title = title_entry.get()
    content = content_entry.get("1.0", tk.END).strip()
    
    if title and content:
        current_time = time.time()
        cursor.execute('''
            INSERT INTO "Note" (title, note, time)
            VALUES (?,?,?)
        ''', (title, content, current_time))

        cursor.execute('''
            INSERT INTO History (All_Question, All_Answer, overall_time)
            VALUES (?,?,?)
        ''', (title, content, current_time))


        connection.commit()
        
        title_entry.delete(0, tk.END)
        content_entry.delete("1.0", tk.END)
        
        result_label.config(text="✓ Note saved!", fg="green")
        window.after(3000, lambda: result_label.config(text=""))
        view_notes()
    else:
        result_label.config(text="✗ Please enter both title and content!", fg="red")

submit_btn = tk.Button(page_notes, text="Submit", command=submit_note, fg="black")
submit_btn.pack(pady=10)

result_label = tk.Label(page_notes, text="", bg="lightgreen")
result_label.pack()

ttk.Separator(page_notes, orient='horizontal').pack(fill='x', pady=10)

tk.Label(page_notes, text="Your Saved Notes:", font=("Arial", 12, "bold"), bg="lightgreen", fg = "#333333").pack()
notes_display = tk.Text(page_notes, height=10, width=70)
notes_display.pack(pady=5)

def view_notes():
    notes_display.delete("1.0", tk.END)
    cursor.execute('SELECT id, title, note, time FROM "Note" ORDER BY id DESC')
    rows = cursor.fetchall()
    
    if not rows:
        notes_display.insert("1.0", "No notes yet. Add your first note above!")
        return
    
    for row in rows:
        note_id, title, note, note_time = row
        from datetime import datetime
        date_str = datetime.fromtimestamp(note_time).strftime("%Y-%m-%d %H:%M")
        
        
        notes_display.insert(tk.END, f"📝 {title}\n")
        notes_display.insert(tk.END, f"   📅 {date_str}\n")
        notes_display.insert(tk.END, f"   📄 {note[:150]}\n")
        notes_display.insert(tk.END, f"   [ID: {note_id}]\n")  # ← 显示 ID
        notes_display.insert(tk.END, "-" * 50 + "\n\n")


tk.Label(page_notes, text="Delete a Note:", font=("Arial", 12, "bold"), bg="lightgreen", fg = "#333333").pack(pady=(10,0))

delete_frame = tk.Frame(page_notes, bg="lightgreen")
delete_frame.pack(pady=5)

tk.Label(delete_frame, text="Enter Note ID to delete:", bg="lightgreen", fg = "#333333").pack(side="left", padx=5)
delete_id_entry = tk.Entry(delete_frame, width=10)
delete_id_entry.pack(side="left", padx=5)

def delete_note():
    try:
        note_id = int(delete_id_entry.get())
        cursor.execute('SELECT id FROM "Note" WHERE id = ?', (note_id,))
        if cursor.fetchone():
            cursor.execute('DELETE FROM "Note" WHERE id = ?', (note_id,))
            connection.commit()
            delete_id_entry.delete(0, tk.END)
            view_notes()  
            result_label.config(text=f" Note {note_id} deleted!", fg="green")
        else:
            result_label.config(text=f" Note {note_id} not found!", fg="red")
    except ValueError:
        result_label.config(text="✗ Please enter a valid ID number!", fg="red")
    
    window.after(3000, lambda: result_label.config(text=""))

delete_btn = tk.Button(delete_frame, text="Delete", command=delete_note, fg="black")
delete_btn.pack(side="left", padx=5)

tk.Label(page_notes, text = "💡 Note IDs are shown in the list below (e.g., [ID: 1])", 
         bg = "lightgreen", font = ("Arial", 9), fg = "black").pack()

view_notes()



# ========== Mistake Tracker ==========

tk.Label(page_mistake, text="Mistake Tracker", font=("Helvetica", 24, "bold"), bg="lightcoral", fg="black").pack(pady=(15,0))

filter_frame = tk.Frame(page_mistake, bg="lightcoral")
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Filter by Function:", bg="lightcoral", fg="black").pack(side="left", padx=5)
function_var = tk.StringVar(value="All")
function_combo = ttk.Combobox(filter_frame, textvariable=function_var, 
    values=["All", "Smart Q&A", "AI Reform"], 
    state="readonly", width=15)
function_combo.pack(side="left", padx=5)

def apply_filter():
    view_mistakes()

filter_btn = tk.Button(filter_frame, text="Apply Filter", command=apply_filter, bg="#4CAF50", fg="black")
filter_btn.pack(side="left", padx=10)

def reset_filter():
    function_var.set("All")
    view_mistakes()

reset_btn = tk.Button(filter_frame, text="Reset", command=reset_filter, bg="#f44336", fg="black")
reset_btn.pack(side="left", padx=5)

tk.Label(page_mistake, text="Past Mistake Questions:", font=("Arial", 13, "bold"), bg="lightcoral", fg="black").pack()
mistake_display = tk.Text(page_mistake, height=30, width=90)
mistake_display.pack(pady=5)

def view_mistakes():
    mistake_display.config(state="normal") 
    mistake_display.delete("1.0", tk.END)
    
    selected_function = function_var.get()
    
    if selected_function == "All":
        cursor.execute('SELECT id, Question, Answer, create_at, Function FROM "training" ORDER BY id DESC')
        rows = cursor.fetchall()
    else:
        cursor.execute('''
            SELECT id, Question, Answer, create_at, Function 
            FROM "training" 
            WHERE Function = ? 
            ORDER BY id DESC
        ''', (selected_function,))
        rows = cursor.fetchall()
    
    if not rows:
        mistake_display.insert("1.0", "No mistakes match your filter!")
        mistake_display.config(state="disabled") 
        return
    
    for row in rows:
        mistake_id, question, answer, created_at, function_name = row
        from datetime import datetime
        date_str = datetime.fromtimestamp(created_at).strftime("%Y-%m-%d %H:%M")
        
        mistake_display.insert(tk.END, f"  Question:\n")
        mistake_display.insert(tk.END, f"   {question}\n")
        mistake_display.insert(tk.END, f" Correct Answer:\n")
        mistake_display.insert(tk.END, f"   {answer}\n")
        mistake_display.insert(tk.END, f"    {date_str}\n")
        mistake_display.insert(tk.END, f"   From Function: {function_name}\n")
        mistake_display.insert(tk.END, f"   [ID: {mistake_id}]\n")
        mistake_display.insert(tk.END, "-" * 70 + "\n\n")

    mistake_display.config(state="disabled")



# ========== History ==========
tk.Label(page_history, text="History", font=("Helvetica", 24, "bold"), bg="lightyellow", fg="black").pack(pady=(15,0))

history_display = tk.Text(page_history, height=70, width=90)
history_display.pack(pady=10)

refresh_btn = tk.Button(page_history, text="Refresh History", command=lambda: refresh_history(), bg="#4CAF50", fg="black")
refresh_btn.pack(pady=5)

def refresh_history():
    history_display.config(state="normal")
    history_display.delete("1.0", tk.END)
    
    try:
        cursor.execute('SELECT id, All_Question, All_Answer, overall_time FROM history ORDER BY id DESC')
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        history_display.insert("1.0", "Database 'history' table not found.")
        history_display.config(state="disabled")
        return
    
    if not rows:
        history_display.insert("1.0", "No history yet. Ask some questions in Training Mode!")
        history_display.config(state="disabled")
        return
    
    for row in rows:
        hid, question, answer, created_at = row
        from datetime import datetime
        date_str = datetime.fromtimestamp(created_at).strftime("%Y-%m-%d %H:%M:%S")
        
        history_display.insert(tk.END, f"Que: {question}\n")
        history_display.insert(tk.END, f"Ans: {answer}\n")
        history_display.insert(tk.END, f"Time: {date_str}\n")
        history_display.insert(tk.END, "-" * 70 + "\n\n")

    history_display.config(state="disabled") 

refresh_history()



# ========== Change page ==========
def switch_page():
    selected = clicked.get()
    
    page_training.pack_forget()
    page_notes.pack_forget()
    page_mistake.pack_forget()
    page_history.pack_forget()
    page_ai_qa.pack_forget()
    page_ai_reform.pack_forget()
    
    if selected == "Training Mode":
        page_training.pack(fill="both", expand=True)
    elif selected == "Note Management":
        page_notes.pack(fill="both", expand=True)
    elif selected == "Mistake Tracker":
        page_mistake.pack(fill="both", expand=True)
        view_mistakes()  
    elif selected == "History":
        page_history.pack(fill="both", expand=True)
        refresh_history()

confirm_btn = tk.Button(window, text="Confirm", command=switch_page, font=("Arial", 12))
confirm_btn.pack(pady=10)
page_training.pack(fill="both", expand=True)

window.mainloop()
connection.close()