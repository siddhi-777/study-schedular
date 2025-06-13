

import random
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

def time_to_float(time_str):
    """Convert 12-hour format (with or without minutes) to float hours."""
    try:
        time_str = time_str.lower()
        if ":" not in time_str:
            if "am" in time_str or "pm" in time_str:
                time_str = time_str.replace("am", " AM").replace("pm", " PM")
            else:
                time_str += " AM"  # Default to AM if not specified
            time_str = time_str.replace(" ", ":00 ")
        else:
            if "am" in time_str or "pm" in time_str:
                time_str = time_str.replace("am", " AM").replace("pm", " PM")
        dt = datetime.strptime(time_str, "%I:%M %p")
        return dt.hour + dt.minute / 60.0
    except ValueError:
        messagebox.showerror("Invalid Input", f"Invalid time format: {time_str}. Use '9 pm' or '9:00 pm'.")
        return None

def to_am_pm(time_float):
    """Convert float hours back to 12-hour format."""
    hour = int(time_float)
    minute = int((time_float - hour) * 60)
    period = "AM" if hour < 12 else "PM"
    hour = hour if 1 <= hour <= 12 else (hour - 12 if hour > 12 else 12)
    return f"{hour}:{minute:02d} {period}"

def generate_time_slots(start, end, session_duration):
    """Create slots of 1 hour with 15-minute break afterwards."""
    slots = []
    while start + session_duration <= end:
        slots.append((start, start + session_duration))
        start += session_duration + 0.25  # 15-minute break
    if end - start >= 0.5:
        slots.append((start, end))
    return slots

def format_hours_minutes(hours):
    """Convert hours to H hours M minutes format."""
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h} hours {m} minutes"

def generate_schedule():
    """Main function to generate and show the study schedule."""
    try:
        wake_up = time_to_float(wake_up_entry.get()) 
        college_start = time_to_float(college_start_entry.get()) 
        college_end = time_to_float(college_end_entry.get()) 
        dinner = time_to_float(dinner_time_entry.get()) 
        sleep = time_to_float(sleep_time_entry.get()) 
        num_subjects = int(num_subjects_entry.get()) 
    except (ValueError, TypeError):
        messagebox.showerror("Invalid Input", "Please enter all fields correctly.")
        return
    
    if None in [wake_up, college_start, college_end, dinner, sleep] or num_subjects <= 0:
        messagebox.showerror("Invalid Input", "Please check your values.")
        return
    
    subjects = []
    for i in range(num_subjects):
        subj = subject_entries[i].get()
        if subj:
            subjects.append(subj)
    if not subjects:
        messagebox.showerror("Invalid Input", "Please enter at least 1 subject.")
        return
    
    morning_slots = generate_time_slots(wake_up + 0.83, college_start - 0.83, 1)
    evening_slots = generate_time_slots(college_end + 1, dinner - 0.17, 1)
    post_dinner_slots = generate_time_slots(dinner + 1, sleep - 0.17, 1)

    time_slots = morning_slots + evening_slots + post_dinner_slots
    
    if not time_slots:
        messagebox.showerror("Invalid Input", "Not enough time to study.")
        return
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    schedule = {day: [] for day in days}

    for day in days:
        used = set()
        for start, end in time_slots:
            available = [s for s in subjects if s not in used]
            if not available:
                available = subjects.copy()
            subject = random.choice(available)
            used.add(subject)
            schedule[day].append((start, end, subject))
  
    show_schedule(schedule, time_slots, days)

def show_schedule(schedule, time_slots, days):
    """Display the final study schedule in a new window."""
    window = tk.Toplevel(root)
    window.title("Study Schedule")
    window.geometry("700x500")
    window.config(bg="#FFFFFF")

    tree = ttk.Treeview(window, columns=['Time'] + days, show='headings')
    tree.heading('Time', text='Time')
    for day in days:
        tree.heading(day, text=day)

    tree.column('Time', width=100)
    for day in days:
        tree.column(day, width=100)

    for start, end in time_slots:
        row = [f"{to_am_pm(start)} - {to_am_pm(end)}"]
        for day in days:
            subject = next((s for s, e, s in schedule[day] if s == start), "N.A.")
            row.append(subject)
        tree.insert('', 'end', values=row)

    tree.pack(fill='both', expand=True)

def create_subject_fields():
    """Dynamically create subject fields based on number of subjects."""
    for widget in subjects_frame.winfo_children():
        widget.destroy()
    subject_entries.clear()
    try:
        num = int(num_subjects_entry.get()) 
    except:
        num = 0
    
    for i in range(num):
        lbl = tk.Label(subjects_frame, text=f"Subject {i+1} :", font=('Helvetica', 10), anchor='w', bg="#FFFFFF")
        lbl.grid(row=i, column=0, sticky='w', pady=2)
        ent = tk.Entry(subjects_frame, width=20)
        ent.grid(row=i, column=1, pady=2, padx=10)
        subject_entries.append(ent)

# Main GUI
root = tk.Tk()
root.title("Study Scheduler")
root.geometry("400x500")
root.config(bg="#FFFFFF")

label = tk.Label(root, text="Study Scheduler", font=('Helvetica', 14, 'bold'), bg="#FFFFFF")
label.pack(pady=10)

frame = tk.Frame(root, bg="#FFFFFF")
frame.pack(pady=10)

labels = ["Wake-up Time (e.g. 6:30 AM or 6 AM)", "College Start Time (e.g. 9 AM)", 
          "College End Time (e.g. 4 pm)", "Dinner Time (e.g. 7 pm)", "Sleep Time (e.g. 11 pm)", 
          "Number of Subjects"]

entries = []
for i, lbl in enumerate(labels):
    l = tk.Label(frame, text=lbl, font=('Helvetica', 10), anchor='w', bg="#FFFFFF")
    l.grid(row=i, column=0, sticky='w', pady=2)
    e = tk.Entry(frame, width=20)
    e.grid(row=i, column=1, pady=2, padx=10)
    entries.append(e)

wake_up_entry, college_start_entry, college_end_entry, dinner_time_entry, sleep_time_entry, num_subjects_entry = entries

subject_entries = []

add_subjects = tk.Button(root, text="Add Subjects", command=create_subject_fields)
add_subjects.pack()

subjects_frame = tk.Frame(root, bg="#FFFFFF")
subjects_frame.pack()

generate_button = tk.Button(root, text="Generate Schedule", command=generate_schedule)
generate_button.pack(pady=20)

root.mainloop()
