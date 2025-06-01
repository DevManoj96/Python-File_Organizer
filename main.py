import tkinter as tk
from tkinter import messagebox, filedialog
import shutil
import os

folder_path = ""
is_dark = False
file_types = {
    "Texts": [".txt", ".doc", ".docx", ".pdf", ".md"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"],
    "Music": [".mp3", ".wav", ".aac", ".ogg", ".flac"],
    "Code": [".py", ".cpp", ".c", ".js", ".html", ".css", ".java", ".php", ".ts", ".cs", ".sh", ".bat", ".json", ".xml"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Executables": [".exe", ".msi", ".apk", ".bin", ".sh"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "Others": []
}

def toggle_theme():
    global is_dark
    is_dark = not is_dark

    bg_color = "#222222" if is_dark else "lightgray"
    fg_color = "white" if is_dark else "black"

    # Apply colors
    root.configure(bg=bg_color)
    heading1.configure(bg=bg_color, fg=fg_color)
    frame.configure(bg=bg_color)
    text_area.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)
    button_frame.configure(bg=bg_color)
    organize_btn.configure(bg=bg_color, fg=fg_color)
    toggle_theme_btn.configure(bg=bg_color, fg=fg_color)
    exit_btn.configure(bg=bg_color, fg=fg_color)



def open_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path: 
        files = os.listdir(folder_path)
        messagebox.showinfo("Folder Selected", f"Folder Selected: {folder_path}")
        text_area.delete("1.0", tk.END)

        for file in files:
            text_area.insert(tk.END, file + "\n")

def organize_files():
    if not folder_path:
        messagebox.showwarning("Warning", "Please select a folder first!")
        return

    folders = {key: os.path.join(folder_path, key) for key in file_types}
    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)

    files = os.listdir(folder_path)

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            moved = False
            for category, extensions in file_types.items():
                if ext in extensions:
                    shutil.move(file_path, os.path.join(folders[category], filename))
                    moved = True
                    break
            if not moved:
                shutil.move(file_path, os.path.join(folders["Others"], filename))

    total_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

    messagebox.showinfo("Done", f"Files have been organized!\nTotal files now: {total_files}")

    open_folder()

# GUI
root = tk.Tk()
root.title("--- Python File Organizer ---")
root.geometry('640x480')
root.resizable(True, True)

heading1 = tk.Label(root, text="Welcome To File Organizer ", font=("Arial", 24, "bold"))
heading1.pack(pady=5)

menubar = tk.Menu(root)
root.config(menu=menubar)
options_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Open Folder", command=open_folder)

frame = tk.Frame(root)
frame.pack()
text_area = tk.Text(frame, wrap=tk.NONE, height=15, width=50)
scrollbar = tk.Scrollbar(frame, orient="vertical", command=text_area.yview)
text_area.configure(yscrollcommand=scrollbar.set)
text_area.pack(side=tk.LEFT)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

button_frame = tk.Frame(root)
button_frame.pack()

organize_btn = tk.Button(button_frame, text="Organize Files", command=organize_files, font=("Arial", 12), width=20, height=2)
organize_btn.pack(pady=5)

toggle_theme_btn = tk.Button(button_frame, text="Toggle Theme", command=toggle_theme, font=("Arial", 12), width=20, height=2)
toggle_theme_btn.pack(pady=5)

exit_btn = tk.Button(button_frame, text="Exit", command=root.quit, font=("Arial", 12), width=20, height=2)
exit_btn.pack(pady=5)

if __name__ == '__main__':
    root.mainloop()
