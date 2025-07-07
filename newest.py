import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def select_file_path():
    """Opens a file dialog to select a file and returns the file path."""
    return filedialog.askopenfilename()

def sort_and_save():
    """Sorts the DataFrame based on column 'D' and saves it to a new file."""
    # Get the file path from the entry widget
    file_path = entry_file.get()
    
    # Basic validation to check if the file path is filled in
    if not file_path:
        messagebox.showerror("Error", "Please select a file.")
        return
    
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Sort the DataFrame based on column 'D'
        df_sorted = df.sort_values(by='diff')
        
        # Write the sorted DataFrame to a new Excel file
        output_path = "sorted_file.xlsx"
        df_sorted.to_excel(output_path, index=False)
        
        messagebox.showinfo("Success", f"File sorted and saved as {output_path}")
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
window = tk.Tk()
window.title("Excel Sorter")
window.geometry("400x200")  # Set window size

label_file = tk.Label(window, text="Select Excel file")
label_file.pack(pady=20)  # Add some padding for better layout

entry_file = tk.Entry(window, width=50)
entry_file.pack(pady=10)

button_browse = tk.Button(window, text="Browse", command=lambda: entry_file.insert(0, select_file_path()))
button_browse.pack()

button_execute = tk.Button(window, text="Sort and Save", command=sort_and_save)
button_execute.pack(pady=20)

window.mainloop()
