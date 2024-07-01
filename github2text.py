import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from github import Github
import base64

class Github2Text:
    def __init__(self, master):
        self.master = master
        master.title("Github2Text")
        master.geometry("800x600")

        self.char_count = tk.StringVar()
        self.char_count.set("Characters: 0")
        self.token_count = tk.StringVar()
        self.token_count.set("Estimated Tokens: 0")

        self.create_widgets()

    def create_widgets(self):
        # URL input
        url_frame = ttk.Frame(self.master)
        url_frame.pack(pady=5, padx=10, fill='x')

        self.url_label = ttk.Label(url_frame, text="Enter GitHub Repo URL:")
        self.url_label.pack(side='left')

        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(side='left', expand=True, fill='x', padx=(5, 0))

        self.fetch_button = ttk.Button(url_frame, text="Fetch Files", command=self.fetch_files)
        self.fetch_button.pack(side='right', padx=(5, 0))

        # Paned window to separate file list and content view
        self.paned_window = ttk.PanedWindow(self.master, orient='horizontal')
        self.paned_window.pack(expand=True, fill='both', pady=5, padx=10)

        # File list frame
        file_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(file_frame, weight=1)

        self.file_canvas = tk.Canvas(file_frame)
        self.file_canvas.pack(side='left', fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(file_frame, orient='vertical', command=self.file_canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.file_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.file_canvas.bind('<Configure>', lambda e: self.file_canvas.configure(scrollregion=self.file_canvas.bbox('all')))

        self.inner_frame = ttk.Frame(self.file_canvas)
        self.file_canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        # Content view frame
        content_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(content_frame, weight=2)

        self.content_text = tk.Text(content_frame, wrap='word', state='disabled')
        self.content_text.pack(expand=True, fill='both')

        # Buttons frame
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=5, padx=10, fill='x')

        self.save_button = ttk.Button(button_frame, text="Save as .txt", command=self.save_files)
        self.save_button.pack(side='left')

        self.token_count_label = ttk.Label(button_frame, textvariable=self.token_count)
        self.token_count_label.pack(side='right', padx=(0, 10))

        self.char_count_label = ttk.Label(button_frame, textvariable=self.char_count)
        self.char_count_label.pack(side='right', padx=(0, 10))

        self.copy_button = ttk.Button(button_frame, text="Copy Content", command=self.copy_content)
        self.copy_button.pack(side='right')

        self.file_vars = []

    def fetch_files(self):
        repo_url = self.url_entry.get()
        try:
            g = Github()
            repo = g.get_repo(repo_url.split('github.com/')[1])
            contents = repo.get_contents("")
            self.files = []

            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    self.files.append(file_content)

            for widget in self.inner_frame.winfo_children():
                widget.destroy()

            self.file_vars = []
            for file in self.files:
                var = tk.BooleanVar(value=True)
                cb = ttk.Checkbutton(self.inner_frame, text=file.path, variable=var, command=self.update_content)
                cb.pack(anchor='w')
                self.file_vars.append((var, file))

            self.file_canvas.update_idletasks()
            self.file_canvas.configure(scrollregion=self.file_canvas.bbox('all'))
            
            self.update_content()  # Update content initially

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_content(self):
        self.content_text.config(state='normal')
        self.content_text.delete('1.0', tk.END)

        selected_files = [file for var, file in self.file_vars if var.get()]
        content = f"Repository: {self.url_entry.get()}\n\n"
        content += "File Structure:\n"
        for file in selected_files:
            content += f"- {file.path}\n"
        content += "\n"

        for file in selected_files:
            content += f"File: {file.path}\n"
            content += "-" * (len(file.path) + 6) + "\n"
            file_content = base64.b64decode(file.content).decode('utf-8')
            content += file_content
            content += "\n\n"

        self.content_text.insert('1.0', content)
        self.content_text.config(state='disabled')
        
        # Update character count and estimated token count
        char_count = len(content)
        token_count = int(char_count / 2.5)
        self.char_count.set(f"Characters: {char_count}")
        self.token_count.set(f"Estimated Tokens: {token_count}")

    def save_files(self):
        content = self.content_text.get('1.0', tk.END)
        if not content.strip():
            messagebox.showwarning("Warning", "No content to save")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not save_path:
            return

        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Repository contents saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_content(self):
        content = self.content_text.get('1.0', tk.END)
        self.master.clipboard_clear()
        self.master.clipboard_append(content)
        messagebox.showinfo("Success", "Content copied to clipboard")

if __name__ == "__main__":
    root = tk.Tk()
    app = Github2Text(root)
    root.mainloop()
