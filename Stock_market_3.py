import requests
from tkinter import *
import customtkinter as ctk
import pandas as pd

api_key = 'UBB7FSMQXUD8AAXS'
entry_info = None  # Initialize entry_info as a global variable

# Initialize the DataFrame outside the function
csv_file_path = r"C:\Users\HP\OneDrive\Desktop\python.project4\Stock market information in the form of an Excel file\CSVfile_excel_2.csv"
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

def search_stock_data():
    global entry_info  # Declare entry_info as a global variable
    selected_date = entry.get()
    selected_time = entry2.get()
    datetime_str = f"{selected_date} {selected_time}:00"

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey={api_key}&datatype=json'

    r = requests.get(url)
    data = r.json()

    if "Time Series (5min)" in data:
        c.delete("all")
        time_series_data = data['Time Series (5min)']

        if datetime_str in time_series_data:
            entry_info = time_series_data[datetime_str]
            display_info = (
                f"Timestamp: {datetime_str}\n"
                f"1. Open: {entry_info['1. open']}\n"
                f"2. High: {entry_info['2. high']}\n"
                f"3. Low: {entry_info['3. low']}\n"
                f"4. Close: {entry_info['4. close']}\n"
                f"5. Volume: {entry_info['5. volume']}"
            )

            c.create_text(250, 250, text=display_info, fill='black', font=('Helvetica', 10), anchor='center')
            error_label.config(text="")

            # Save to CSV directly without user input
            save_to_csv(datetime_str)
        else:
            error_label.config(text=f"No data available for {datetime_str}")
    else:
        error_label.config(text="Error: Unable to retrieve Time Series (5min) data from the API.")

def save_to_csv(datetime_str):
    global entry_info, df  # Access entry_info and df as global variables
    if entry_info is not None:
        try:
            # Append data to the DataFrame
            new_row = pd.DataFrame({
                'Timestamp': [datetime_str],
                'Open': [float(entry_info['1. open'])],
                'High': [float(entry_info['2. high'])],
                'Low': [float(entry_info['3. low'])],
                'Close': [float(entry_info['4. close'])],
                'Volume': [int(entry_info['5. volume'])]
            })
            df = pd.concat([df, new_row], ignore_index=True)

            # Save the DataFrame back to the CSV file
            df.to_csv(csv_file_path, index=False)
            error_label.config(text=f"Data appended to {csv_file_path}")
        except Exception as e:
            error_label.config(text=f"Error: {str(e)}")
    else:
        error_label.config(text="Error: No stock data available. Search for data first.")

# Graphics
root = Tk()
root.title("Stock Market")
root.geometry("500x500")  
c = Canvas(root, width=500, height=400, bg='silver')
c.pack()

frame1 = Frame(c, bg='gray', bd=5)
frame1.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

label = Label(frame1, text="Enter the date:", bg='gray', fg='black')
label.pack(side='left')

entry = ctk.CTkEntry(frame1)
entry.pack(side='left')

frame2 = Frame(c, bg='gray', bd=5)
frame2.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.1, anchor='n')

label2 = Label(frame2, text="Enter the hour: ", bg='gray', fg='black')
label2.pack(side="left")

entry2 = ctk.CTkEntry(frame2)
entry2.pack(side="left")

frame_search_button = Frame(c, bg='gray', bd=5)
frame_search_button.place(relx=0.5, rely=0.4, relwidth=0.75, relheight=0.1, anchor='n')

search_btn = Button(frame_search_button, text="Search", command=search_stock_data)
search_btn.pack(side="top")  

error_label = Label(c, text="",bg="silver", fg='red')
error_label.place(relx=0.5, rely=0.9, anchor='n')

root.mainloop()
