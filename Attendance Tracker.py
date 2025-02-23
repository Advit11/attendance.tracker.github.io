import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
from datetime import datetime, timedelta
from collections import Counter, defaultdict

class Attendance:
    def __init__(self):
        self.filename = "attendance.csv"

    def mark_attendance(self, name):
        with open(self.filename, 'a', newline='') as csvfile:
            fieldnames = ['Name', 'Date', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'Name': name, 'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Status': 'Present'})

    def sign_out_all(self):
        try:
            with open(self.filename, 'r') as csvfile:
                reader = list(csv.DictReader(csvfile))
            with open(self.filename, 'w', newline='') as csvfile:
                fieldnames = ['Name', 'Date', 'Status', 'Duration']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    if row['Status'] == 'Present':
                        sign_in_time = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
                        duration = datetime.now() - sign_in_time
                        row['Status'] = 'No Meeting'
                        row['Duration'] = str(duration.total_seconds())
                    writer.writerow(row)
        except FileNotFoundError:
            pass

    def clear_leaderboard(self):
        with open(self.filename, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Date', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

class AttendanceApp:
    def __init__(self, root):
        self.attendance = Attendance()
        self.root = root
        self.root.title("Attendance System")
        self.root.configure(bg='light blue')

        self.frame = tk.Frame(root, bg='light blue')
        self.frame.pack(expand=True)

        self.name_label = tk.Label(self.frame, text="Name", bg='light blue', fg='black', font=('Arial', 12))
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.name_entry = tk.Entry(self.frame, font=('Arial', 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.mark_button = tk.Button(self.frame, text="Mark Attendance", command=self.mark_attendance, relief='solid', bd=2, font=('Arial', 12), bg='light green')
        self.mark_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.view_button = tk.Button(self.frame, text="View Attendance", command=self.view_attendance, relief='solid', bd=2, font=('Arial', 12))
        self.view_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.leaderboard_button = tk.Button(self.frame, text="View Leaderboard", command=self.view_leaderboard, relief='solid', bd=2, font=('Arial', 12))
        self.leaderboard_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.sign_out_button = tk.Button(self.frame, text="Sign Out All", command=self.sign_out_all, relief='solid', bd=2, font=('Arial', 12))
        self.sign_out_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.clear_leaderboard_button = tk.Button(self.frame, text="Clear Leaderboard", command=self.clear_leaderboard, relief='solid', bd=2, font=('Arial', 12))
        self.clear_leaderboard_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def mark_attendance(self):
        name = self.name_entry.get()
        if name:
            self.attendance.mark_attendance(name)
            messagebox.showinfo("Success", "Attendance marked successfully")
        else:
            messagebox.showwarning("Input Error", "Please enter a name")

    def view_attendance(self):
        try:
            with open(self.attendance.filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                records = "\n".join([f"{row['Name']} - {row['Date']} - {row['Status']}" for row in reader])
                messagebox.showinfo("Attendance Records", records if records else "No records found")
        except FileNotFoundError:
            messagebox.showwarning("File Not Found", "No attendance records found")

    def view_leaderboard(self):
        try:
            with open(self.attendance.filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                attendance_count = Counter(row['Name'] for row in reader)
                duration_count = defaultdict(timedelta)
                for row in reader:
                    if 'Duration' in row and row['Duration']:
                        duration_count[row['Name']] += timedelta(seconds=float(row['Duration']))
                leaderboard = "\n".join([f"{name}: {count} times" for name, count in attendance_count.most_common()])
                messagebox.showinfo("Attendance Leaderboard", leaderboard if leaderboard else "No records found")
        except FileNotFoundError:
            messagebox.showwarning("File Not Found", "No attendance records found")

    def sign_out_all(self):
        self.attendance.sign_out_all()
        messagebox.showinfo("Success", "All attendees have been signed out")

    def clear_leaderboard(self):
        if messagebox.askyesno("Clear Leaderboard", "Are you sure you want to clear the leaderboard?"):
            self.attendance.clear_leaderboard()
            messagebox.showinfo("Success", "Leaderboard has been cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
