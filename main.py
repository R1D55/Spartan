import smtplib
import random
from flask import Flask, request, render_template, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from PIL import Image, ImageTk

# Initialize Flask app
app = Flask(__name__)  # <-- Make sure this line is present

# Example function for chatbot response
def get_chatbot_response(user_input, user_email=None):
    # Here, you can call your existing chatbot logic to generate responses
    if "leave policy" in user_input.lower():
        return "Our leave policy includes 20 annual leaves, 10 sick leaves, and 5 casual leaves per year."
    else:
        return "Sorry, I couldn't understand that. Could you clarify?"

# Route for rendering the chatbot web page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle user input and return chatbot response (as JSON)
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get("message")
    user_email = request.json.get("email", None)  # Optional email parameter
    response = get_chatbot_response(user_input, user_email)
    return jsonify({"response": response})

# Example user login (if needed)
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get("email")
    # Implement logic to handle login and return status
    return jsonify({"status": "success", "message": "Logged in successfully", "email": email})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True) 

# Function to validate the query input
def validate_query(query):
    try:
        int(query.split()[-1])
        return True
    except ValueError:
        return False

# Function to handle user queries
def query_chatbot():
    query = user_input.get("1.0", "end-1c")
    if not validate_query(query):
        chatbot_output.config(state=tk.NORMAL)
        chatbot_output.insert(tk.END, "Invalid query. Please enter a valid employee ID.\n\n")
        chatbot_output.config(state=tk.DISABLED)
        return

    employee_id = int(query.split()[-1])
    
    
    chatbot_output.config(state=tk.NORMAL)
    chatbot_output.insert(tk.END, f"You: {query}\n", "user")
    
    chatbot_output.config(state=tk.DISABLED)

# Function to save chat conversation to a file
def save_chat():
    chat_content = chatbot_output.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(chat_content)

# Function to display a welcome message when the chatbot starts
def show_welcome_message():
    chatbot_output.config(state=tk.NORMAL)
    chatbot_output.insert(tk.END, "Welcome to the Employee Chatbot! How can I assist you today?\n\n", "chatbot")
    chatbot_output.config(state=tk.DISABLED)

# Function to clear the chat output
def clear_chat():
    chatbot_output.config(state=tk.NORMAL)
    chatbot_output.delete("1.0", tk.END)
    chatbot_output.config(state=tk.DISABLED)

# Function to upload document and display its content
def upload_document():
    # Open file dialog to select a file
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", ".txt"), ("PDF files", ".pdf"), ("Word files", "*.docx")]
    )
    
    # If a file is selected, process it
    if file_path:
        # Call a function to extract content from the selected document
        doc_content = extract_document_content(file_path)
        
        if doc_content:
            chatbot_output.config(state=tk.NORMAL)
            chatbot_output.insert(tk.END, f"\nDocument content:\n{doc_content}\n\n", "chatbot")
            chatbot_output.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "Could not extract content from the document.")
    else:
        messagebox.showinfo("Info", "No document selected.")

# Function to extract content from a document
def extract_document_content(file_path):
    if file_path.endswith('.txt'):
        return extract_text_file(file_path)
    elif file_path.endswith('.pdf'):
        return extract_pdf_file(file_path)
    elif file_path.endswith('.docx'):
        return extract_docx_file(file_path)
    else:
        return None

# Function to extract text from a .txt file
def extract_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading text file: {e}")
        return None

# Function to extract text from a PDF file (You need to install PyPDF2)
def extract_pdf_file(file_path):
    try:
        import PyPDF2
        pdf_file = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        text = ""
        for page in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page).extract_text()
        pdf_file.close()
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

# Function to extract text from a Word document (You need to install python-docx)
def extract_docx_file(file_path):
    try:
        import docx
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading Word document: {e}")
        return None

# Function to send 2FA code to the user's email
def send_2fa_code(email):
    # Generate a random 6-digit 2FA code
    global verification_code
    verification_code = str(random.randint(100000, 999999))

    # Set up email message
    msg = MIMEMultipart()
    msg['From'] = "atulk4360@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Your 2FA Code"
    body = f"Your 2FA code is: {verification_code}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up email server (Gmail example; change based on provider)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("atulk4360@gmail.com", "igus ymzm bbzu oprj")  # Replace with your credentials
        text = msg.as_string()
        server.sendmail("atulk4360@gmail.com", email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Function to validate 2FA code entered by the user
def validate_2fa_code():
    entered_code = code_input.get()
    if entered_code == verification_code:
        # Hide 2FA frame and show chatbot input, buttons, and output
        frame_2fa.pack_forget()
        frame_input.pack(pady=10)  # Show chatbot input
        frame_buttons.pack(pady=5)  # Show buttons (upload, save, clear)
        chatbot_output.pack(pady=10)  # Show output area
        show_welcome_message()  # Optional: Display a welcome message
    else:
        messagebox.showerror("Error", "Invalid 2FA code")

# Function to handle email login
def login():
    email = email_input.get()
    if send_2fa_code(email):
        # Hide email login and show 2FA frame
        frame_login.pack_forget()
        frame_2fa.pack(pady=10)
    else:
        messagebox.showerror("Error", "Failed to send 2FA code. Please try again.")

# Create Tkinter window
window = tk.Tk()
window.title("Gail ChatBot")
window.geometry("600x700")

# Function to handle email login
def login():
    email = email_input.get()
    if send_2fa_code(email):
        # Hide email login and show 2FA frame
        frame_login.pack_forget()
        frame_2fa.pack(pady=10)
    else:
        messagebox.showerror("Error", "Failed to send 2FA code. Please try again.")

# Function to handle logout
def logout():
    # Hide chatbot input, buttons, and output
    frame_input.pack_forget()
    frame_buttons.pack_forget()
    chatbot_output.pack_forget()
    # Show email login frame
    frame_login.pack(pady=10)

# Frame for email login
frame_login = tk.Frame(window)
email_label = tk.Label(frame_login, text="Enter your email:")
email_label.pack(pady=5)
email_input = tk.Entry(frame_login, width=30)
email_input.pack(pady=5)
login_button = tk.Button(frame_login, text="Login", command=login)
login_button.pack(pady=5)
frame_login.pack(pady=10)

# Frame for 2FA input
frame_2fa = tk.Frame(window)
code_label = tk.Label(frame_2fa, text="Enter the 2FA code sent to your email:")
code_label.pack(pady=5)
code_input = tk.Entry(frame_2fa, width=30)
code_input.pack(pady=5)
verify_button = tk.Button(frame_2fa, text="Verify", command=validate_2fa_code)
verify_button.pack(pady=5)



# Initially hide the chatbot input, buttons, and output
frame_input = tk.Frame(window)
frame_input.pack_forget()

user_input = tk.Text(frame_input, height=5, width=50)
user_input.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(frame_input, text="Send Query", command=query_chatbot)
send_button.pack(side=tk.LEFT, padx=5)

frame_buttons = tk.Frame(window)
frame_buttons.pack_forget()

clear_button = tk.Button(frame_buttons, text="Clear Chat", command=clear_chat)
clear_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(frame_buttons, text="Save Chat", command=save_chat)
save_button.pack(side=tk.LEFT, padx=5)

upload_button = tk.Button(frame_buttons, text="Upload Document", command=upload_document)
upload_button.pack(side=tk.LEFT, padx=5)

# Add logout button
logout_button = tk.Button(frame_buttons, text="Logout", command=logout)
logout_button.pack(side=tk.LEFT, padx=5)

chatbot_output = tk.Text(window, height=20, width=70)
chatbot_output.pack(pady=10)
chatbot_output.config(state=tk.DISABLED)

# Call welcome message function
# show_welcome_message()

# Start with the email login screen
frame_login.pack(pady=10)


# Run Tkinter main loop
window.mainloop()