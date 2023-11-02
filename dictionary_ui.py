"""This code will create a GUI with another supporting GUI, 
collects CSV data 
and dumps into JSON file."""

# Import needed packages
import csv
import json
import tkinter as tk
from tkinter import messagebox

# Create function to quit application
def quit_application(application):
    """
    param: Application name
    paramType: Tkinter App
    return: None
    returnType: None
    """
    application.destroy()


# Function to read from list and dumps into JSON
def dump_data(sales_data):
    """
    param: List of Dictionaries
    paramType: List
    return: None
    returnType: None
    """
    with open("transaction_data.json", mode='w', encoding="utf-8") as file:
        json.dump(sales_data, file, indent=4)


# Function to write to CSV File
def write_to_csv(filename):
    """
    param: Filename of CSV File
    paramType: String
    return: List of data
    returnType: List
    """
    message_box.config(state="normal")
    welcome_label.config(text="Enter New Data in Box Below\nEach Field Separated By a Comma!")
    new_data = message_box.get("1.0", "end-1c").splitlines()
    if not new_data:
        return
    with open(filename, mode='a', newline='', encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        for data_row in new_data:
            data_to_add = data_row.split(',')
            if len(data_to_add) != 8:
                messagebox.showerror("Error", "Not Enough Data. Fields Must Be 8 Feilds!")
                return
            csv_writer.writerow(data_to_add)
            message_box.delete("1.0", "end")
    welcome_label.config(text="Data Added! Click Add Button To Add More Data.")
    data = read_from_csv(filename)
    dump_data(data)
    message_box.config(state="disabled")

# Function to read from CSV File into list
def read_from_csv(filename):
    """
    param: Filename of CSV File
    paramType: String
    return: List of data
    returnType: List
    """
    sales_data = []
    with open(filename, mode='r', encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # Clean up extra quote characters from each piece of data
            cleaned_row = [item.strip('"') for item in row]
            # Create a dictionary for the current line
            data_dict = {
                "Transaction_date": cleaned_row[0],
                "Product": cleaned_row[1],
                "Price": int(cleaned_row[2]),
                "Payment_Type": cleaned_row[3],
                "Name": cleaned_row[4],
                "City": cleaned_row[5],
                "State": cleaned_row[6],
                "Country": cleaned_row[7],
            }
            sales_data.append(data_dict)
        dump_data(sales_data)
    return sales_data


# Function to create supporting window, reads data and adds data from and toCSV
def fetch_data():
    """
    param: None
    paramType: None
    return: None
    returnType: None
    """

    # Call function to get data
    data = read_from_csv("SalesJan2009.csv")

    # Create variables and window
    supporting_app = tk.Toplevel(app)
    supporting_app.title("Transactions Made Easier: Fetch Data")
    supporting_app.geometry("750x500+1000+100")
    message_box_support = tk.Text(supporting_app, height=10, width=100, state="normal")
    welcome_label_support = tk.Label(supporting_app, text="Fetched Data!")
    welcome_label_support.pack(padx=5, pady=5)
    message_box_support.pack(padx=5, pady=5)
    quit_button_support = tk.Button(supporting_app, text="Done")
    quit_button_support.pack(padx=5, pady=5)

    # Configure variables
    supporting_app.config(background="darkgreen")
    welcome_label_support.config(background="darkgreen", fg="#ffee27", font="Verdana")
    message_box_support.config(background="#918500")
    quit_button_support.config(background="#918500",
                       command=lambda: quit_application(supporting_app))

    # Print data onto message box
    for data_row in data:
        formatted_row = [word.title() if not str(
            word).isdigit() else str(word) for word in data_row.values()]
        message_box_support.insert("end", ", ".join(formatted_row) + '\n')
    # Disable message box to avoid butchered data
    message_box_support.config(state="disabled")


# Create windows and variables
app = tk.Tk()
app.title("Transactions Made Easier")
app.geometry("750x500+200+100")
message_box = tk.Text(app, height=10, width=100, state="disabled")
welcome_label = tk.Label(app, text="Welcome to Transaction Made Easier!")
fetch_data_button = tk.Button(app, text="Fetch Data", command=fetch_data)
quit_button = tk.Button(app, text="Quit Application")
add_button = tk.Button(app, text="Add New Data")

# Configure variables
app.config(background="darkgreen")
welcome_label.config(background="darkgreen", fg="#ffee27", font="Verdana")
message_box.config(background="#918500")
fetch_data_button.config(background="#918500")
quit_button.config(background="#918500", command=lambda: quit_application(app))
add_button.config(background="#918500",
                  command=lambda: write_to_csv("SalesJan2009.csv"))


welcome_label.pack(padx=5, pady=5)
message_box.pack(padx=5, pady=5)
fetch_data_button.pack(padx=5, pady=5)
add_button.pack(padx=5, pady=5)
quit_button.pack(padx=5, pady=50)
app.mainloop()
