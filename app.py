import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


# Function to generate the receipt and table display
def generate_receipt():
    # Getting all the input values
    school_name = "REJENDRA PRASAD TARACHNAD P.G. COLLEGE"
    address = "Paragpur Nihlaul"
    receipt_no = entry_receipt_no.get()
    student_name = entry_name.get()
    gender = gender_var.get()
    session = entry_session.get()
    father_name = entry_father_name.get()
    student_class = entry_class.get()
    exam_fee = entry_exam_fee.get()
    project_fee = entry_project_fee.get()

    # Validate fees
    try:
        exam_fee = float(exam_fee)
        project_fee = float(project_fee) if project_fee else 0.0
    except ValueError:
        messagebox.showerror("Error", "Fees should be valid numbers!")
        return

    # Total fee, deposited, and due calculations
    total_fee = exam_fee + project_fee
    deposited = float(entry_deposited.get()) if entry_deposited.get() else 0.0
    due = total_fee - deposited
    
    # Current date
    current_date = date.today().strftime("%d-%m-%Y")

    # Update the Excel-like grid
    treeview.insert('', 'end', values=(receipt_no, student_name, gender, session, father_name, student_class, exam_fee, project_fee, total_fee, deposited, due))


# Function to save the receipt as a colorful PDF with tables
def save_as_pdf():
    # Ensure school_name is properly defined
    school_name = "REJENDRA PRASAD TARACHNAD P.G. COLLEGE"
    address = "Paragpur Nihlaul"
    
    # Getting all the input values again
    receipt_no = entry_receipt_no.get()
    student_name = entry_name.get()
    gender = gender_var.get()
    session = entry_session.get()
    father_name = entry_father_name.get()
    student_class = entry_class.get()
    exam_fee = entry_exam_fee.get()
    project_fee = entry_project_fee.get()

    # Check required fields
    if not receipt_no or not student_name or not exam_fee:
        messagebox.showerror("Error", "Please fill all required fields (Receipt No, Student Name, Exam Fee).")
        return

    try:
        exam_fee = float(exam_fee)
        project_fee = float(project_fee) if project_fee else 0.0
    except ValueError:
        messagebox.showerror("Error", "Fees should be valid numbers!")
        return

    # Total fee, deposited, and due calculations
    total_fee = exam_fee + project_fee
    deposited = float(entry_deposited.get()) if entry_deposited.get() else 0.0
    due = total_fee - deposited
    
    current_date = date.today().strftime("%d-%m-%Y")
    
    # Create PDF
    pdf_file = f"Receipt_{receipt_no}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Adding details to PDF
    c.setFont("Helvetica-Bold", 18)
    c.drawString(30, 750, f"{school_name.upper()}")  # Using the school_name variable here
    c.setFont("Helvetica", 12)
    c.drawString(30, 730, f"{address}")
    
    c.drawString(30, 690, f"Receipt No: {receipt_no}")
    c.drawString(30, 670, f"Date: {current_date}")
    
    c.drawString(30, 630, f"Student Name: {student_name}")
    c.drawString(30, 610, f"Gender: {gender}")
    c.drawString(30, 590, f"Session: {session}")
    c.drawString(30, 570, f"Father's Name: {father_name}")
    c.drawString(30, 550, f"Class: {student_class}")
    c.drawString(30, 530, f"Exam Fee: ${exam_fee:.2f}")
    c.drawString(30, 510, f"Project Fee: ${project_fee:.2f}")
    
    c.drawString(30, 470, f"Total Fee: ${total_fee:.2f}")
    c.drawString(30, 450, f"Deposited: ${deposited:.2f}")
    c.drawString(30, 430, f"Due: ${due:.2f}")
    
    c.drawString(30, 390, "Thank you for your payment!")
    
    # Create a table with colored headers and rows
    table_data = [
        ["Receipt No", "Student Name", "Gender", "Session", "Father Name", "Class", "Exam Fee", "Project Fee", "Total Fee", "Deposited", "Due"],
        [receipt_no, student_name, gender, session, father_name, student_class, f"${exam_fee:.2f}", f"${project_fee:.2f}", f"${total_fee:.2f}", f"${deposited:.2f}", f"${due:.2f}"]
    ]
    
    # Positioning for the table
    x = 30
    y = 400
    row_height = 20
    col_widths = [100, 150, 70, 80, 150, 60, 80, 80, 80, 80, 80]
    
    # Header row (colored background and white text)
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    c.rect(x, y, sum(col_widths), row_height, fill=1)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.white)
    
    # Draw the table header
    for i, header in enumerate(table_data[0]):
        c.drawString(x + sum(col_widths[:i]) + 5, y + 5, header)
    
    y -= row_height  # Move down after header
    
    # Data rows (alternate background color)
    c.setFont("Helvetica", 10)
    for row_idx, row in enumerate(table_data[1:]):
        if row_idx % 2 == 0:
            c.setFillColor(colors.lightgrey)  # Light grey for even rows
        else:
            c.setFillColor(colors.white)  # White for odd rows
        
        c.rect(x, y, sum(col_widths), row_height, fill=1)
        c.setFillColor(colors.black)
        
        for col_idx, cell in enumerate(row):
            c.drawString(x + sum(col_widths[:col_idx]) + 5, y + 5, str(cell))
        
        y -= row_height  # Move down for the next row
    
    # Save the PDF
    c.save()

    # Inform user
    messagebox.showinfo("PDF Saved", f"Receipt saved as {pdf_file}")


# Setting up the main window
root = tk.Tk()
root.title("School Receipt Generator")
root.geometry("800x750")
root.config(bg="white")  # White background for the window

# Add a title label with colorful style
title_label = tk.Label(root, text="School Receipt Generator", font=("Helvetica", 20, "bold"), bg="white", fg="black")
title_label.pack(pady=10, fill='x')

# Add the school name and address with large fonts and bold style
school_name_label = tk.Label(root, text="REJENDRA PRASAD TARACHNAD P.G. COLLEGE", font=("Helvetica", 18, "bold"), bg="white", fg="black")
school_name_label.pack(pady=5)

address_label = tk.Label(root, text="Paragpur Nihlaul", font=("Helvetica", 14), bg="white", fg="black")
address_label.pack(pady=5)

# Create a frame for the form inputs with a white background
form_frame = tk.Frame(root, bg="white", padx=20, pady=20)
form_frame.pack(pady=20, padx=10)

# Color black for all labels
label_color = "black"

# Add the labels and entry fields inside the frame with a blue layout
label_receipt_no = tk.Label(form_frame, text="Receipt No:", font=("Helvetica", 12), fg=label_color, bg="white")
label_receipt_no.grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_receipt_no = tk.Entry(form_frame, font=("Helvetica", 12))
entry_receipt_no.grid(row=0, column=1, padx=10, pady=5)

label_name = tk.Label(form_frame, text="Student Name:", font=("Helvetica", 12), fg=label_color, bg="white")
label_name.grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_name = tk.Entry(form_frame, font=("Helvetica", 12))
entry_name.grid(row=1, column=1, padx=10, pady=5)

gender_var = tk.StringVar()
label_gender = tk.Label(form_frame, text="Gender:", font=("Helvetica", 12), fg=label_color, bg="white")
label_gender.grid(row=2, column=0, sticky="w", padx=10, pady=5)
gender_male = tk.Radiobutton(form_frame, text="Male", variable=gender_var, value="Male", font=("Helvetica", 12), bg="white", fg="black")
gender_female = tk.Radiobutton(form_frame, text="Female", variable=gender_var, value="Female", font=("Helvetica", 12), bg="white", fg="black")
gender_male.grid(row=2, column=1, padx=10, pady=5)
gender_female.grid(row=2, column=2, padx=10, pady=5)

label_session = tk.Label(form_frame, text="Session:", font=("Helvetica", 12), fg=label_color, bg="white")
label_session.grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_session = tk.Entry(form_frame, font=("Helvetica", 12))
entry_session.grid(row=3, column=1, padx=10, pady=5)

label_father_name = tk.Label(form_frame, text="Father's Name:", font=("Helvetica", 12), fg=label_color, bg="white")
label_father_name.grid(row=4, column=0, sticky="w", padx=10, pady=5)
entry_father_name = tk.Entry(form_frame, font=("Helvetica", 12))
entry_father_name.grid(row=4, column=1, padx=10, pady=5)

label_class = tk.Label(form_frame, text="Class:", font=("Helvetica", 12), fg=label_color, bg="white")
label_class.grid(row=5, column=0, sticky="w", padx=10, pady=5)
entry_class = tk.Entry(form_frame, font=("Helvetica", 12))
entry_class.grid(row=5, column=1, padx=10, pady=5)

label_exam_fee = tk.Label(form_frame, text="Exam Fee:", font=("Helvetica", 12), fg=label_color, bg="white")
label_exam_fee.grid(row=6, column=0, sticky="w", padx=10, pady=5)
entry_exam_fee = tk.Entry(form_frame, font=("Helvetica", 12))
entry_exam_fee.grid(row=6, column=1, padx=10, pady=5)

label_project_fee = tk.Label(form_frame, text="Project Fee:", font=("Helvetica", 12), fg=label_color, bg="white")
label_project_fee.grid(row=7, column=0, sticky="w", padx=10, pady=5)
entry_project_fee = tk.Entry(form_frame, font=("Helvetica", 12))
entry_project_fee.grid(row=7, column=1, padx=10, pady=5)

label_deposited = tk.Label(form_frame, text="Deposited:", font=("Helvetica", 12), fg=label_color, bg="white")
label_deposited.grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_deposited = tk.Entry(form_frame, font=("Helvetica", 12))
entry_deposited.grid(row=8, column=1, padx=10, pady=5)

# Add buttons to generate and save receipt
button_generate = tk.Button(root, text="Generate Receipt", font=("Helvetica", 14), bg="#4CAF50", fg="white", command=generate_receipt)
button_generate.pack(pady=10, padx=20, fill="x")

button_save_pdf = tk.Button(root, text="Save as PDF", font=("Helvetica", 14), bg="#2196F3", fg="white", command=save_as_pdf)
button_save_pdf.pack(pady=10, padx=20, fill="x")


# Create a Treeview for the table view
columns = ("Receipt No", "Student Name", "Gender", "Session", "Father Name", "Class", "Exam Fee", "Project Fee", "Total Fee", "Deposited", "Due")
treeview = ttk.Treeview(root, columns=columns, show="headings", style="Treeview")
treeview.pack(pady=20, padx=20)

# Treeview styling for black background with white text
style = ttk.Style()
style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
style.configure("Treeview.Heading", background="black", foreground="white")

# Run the main loop
root.mainloop()
