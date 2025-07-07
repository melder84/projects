import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def select_file_path():
    """Opens a file dialog to select a file and returns the file path."""
    return filedialog.askopenfilename()

def execute_comparison():
    """Executes the file comparison operation."""
    # Get file paths from entry widgets
    file1 = entry_file1.get()
    file2 = entry_file2.get()

    # Basic validation to check if file paths are filled in
    if not file1 or not file2:
        messagebox.showerror("Error", "Please select both files.")
        return

    try:
        # Reading the Excel files, assuming the first row is NOT a header
        df1 = pd.read_excel(file1, header=None)
        df2 = pd.read_excel(file2, header=None)

        # Convert the relevant columns to the expected types before merging
        df1[0] = df1[0].astype(str)
        df2[0] = df2[0].astype(str)
        df2[5] = pd.to_numeric(df2[5], errors='coerce')  # Assumed column 'F' is at index 5

        # Merge on the common column
        merged_df = pd.merge(df1, df2[[0, 5]], on=0, how='inner', suffixes=('', '_y'))

        # Check if the columns are as expected after the merge
        if merged_df.empty:
            raise ValueError("No matching data found or the files are not structured as expected.")

        # Retrieve the column names after merging, no longer assuming their indices
        column_names = merged_df.columns.tolist()
        print("Column names after merge:", column_names)  # Debug information

        # Identify columns by names rather than fixed indices
        column_on_hand = merged_df.columns[1]  # Assuming this is 'B' from df1
        column_nav = merged_df.columns[-1]  # Assuming 'F' from df2 is the last column in the merged result

        # Convert 'On Hand' column to numeric values, handling non-numeric gracefully
        merged_df[column_on_hand] = pd.to_numeric(merged_df[column_on_hand], errors='coerce')

        # Calculate differences and build a list of rows with differences
        differences = []
        for index, row in merged_df.iterrows():
            difference = row[column_on_hand] - row[column_nav]
            if not pd.isna(difference) and difference != 0:
                # Constructing a dictionary for each row with a difference
                row_dict = {
                    'Product': row[0],
                    'On Hand': row[column_on_hand],
                    'Nav': row[column_nav],
                    'Difference': difference
                }
                differences.append(row_dict)

        # If there are differences, save them to a new Excel file
        if differences:
            differences_df = pd.DataFrame(differences)
            differences_df.to_excel("differences.xlsx", index=False)
            messagebox.showinfo("Success", "Differences found and saved successfully!")
        else:
            messagebox.showinfo("No Differences", "There are no differences between the selected columns for the matched products.")

    except Exception as e:
        print(f"An error occurred: {e}")  # More detailed console error message
        messagebox.showerror("Error", str(e))

# GUI setup
window = tk.Tk()
window.title("Inventory Comparison Tool")



label_file1 = tk.Label(window, text="On hand file")
label_file1.pack()

entry_file1 = tk.Entry(window, width=50)
entry_file1.pack()

button_browse1 = tk.Button(window, text="Browse", command=lambda: entry_file1.insert(0, select_file_path()))
button_browse1.pack()

label_file2 = tk.Label(window, text="Nav file")
label_file2.pack()

entry_file2 = tk.Entry(window, width=50)
entry_file2.pack()

button_browse2 = tk.Button(window, text="Browse", command=lambda: entry_file2.insert(0, select_file_path()))
button_browse2.pack()

button_execute = tk.Button(window, text="Execute Comparison", command=execute_comparison)
button_execute.pack()




window.mainloop()
