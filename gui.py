import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import server
import utils
import downloader
import socket


def get_lan_ip():
    """Return LAN IP address, fallback to localhost if error."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def run_app():
    root = tk.Tk()
    root.title("WHOIST3ASHARE")
    root.geometry("400x400")
    root.resizable(False, False)

    # Tabs
    notebook = ttk.Notebook(root)
    host_frame = tk.Frame(notebook)
    client_frame = tk.Frame(notebook)

    notebook.add(host_frame, text="Host (Share Files)")
    notebook.add(client_frame, text="Client (Download Files)")
    notebook.pack(expand=True, fill="both")

    # -------------------
    # Host Mode
    # -------------------
    current_port = None
    current_urls = None

    def choose_folder():
        nonlocal current_port, current_urls
        folder = filedialog.askdirectory()
        if folder:
            port = server.start_server(folder)
            ip = utils.get_local_ip()

            localhost_url = f"http://127.0.0.1:{port}/"
            lan_url = f"http://{ip}:{port}/"
            current_port = port
            current_urls = f"Localhost: {localhost_url}\nLAN: {lan_url}"

            messagebox.showinfo(
                "Server Started", f"Serving:\n{folder}\n\nURLs:\n{current_urls}"
            )
            copy_button.config(state="normal")

    def stop_server():
        server.stop_server()
        messagebox.showinfo("Server Stopped", "File sharing stopped.")
        copy_button.config(state="disabled")

    def copy_urls():
        if current_urls:
            root.clipboard_clear()
            root.clipboard_append(current_urls)
            root.update()
            messagebox.showinfo("Copied", "URLs copied to clipboard!")

    tk.Label(
        host_frame, text="Share your folder over LAN", font=("Arial", 12, "bold")
    ).pack(pady=10)
    tk.Button(
        host_frame,
        text="Start Sharing",
        command=choose_folder,
        width=20,
        height=2,
        bg="#4CAF50",
        fg="white",
    ).pack(pady=10)
    tk.Button(
        host_frame,
        text="Stop Sharing",
        command=stop_server,
        width=20,
        height=2,
        bg="#f44336",
        fg="white",
    ).pack(pady=10)

    copy_button = tk.Button(
        host_frame,
        text="Copy URLs",
        command=copy_urls,
        width=20,
        height=2,
        bg="#2196F3",
        fg="white",
        state="disabled",
    )
    copy_button.pack(pady=10)

    # -------------------
    # Client Mode
    # -------------------
    file_list = tk.Listbox(client_frame, width=50, height=10)
    file_list.pack(pady=10)

    url_entry = tk.Entry(client_frame, width=40)
    url_entry.insert(0, "http://")
    url_entry.pack(pady=5)

    def fetch_files():
        url = url_entry.get().strip()
        files = downloader.list_files(url)
        file_list.delete(0, tk.END)
        for f in files:
            file_list.insert(tk.END, f)

    def download_selected():
        url = url_entry.get().strip()
        selected = file_list.curselection()
        if not selected:
            messagebox.showwarning("No file", "Please select a file to download.")
            return
        filename = file_list.get(selected[0])
        save_dir = filedialog.askdirectory(title="Select download folder")
        if save_dir:
            result = downloader.download_file(url, filename, save_dir)
            messagebox.showinfo("Download", result)

    tk.Label(client_frame, text="Enter host URL:", font=("Arial", 12)).pack(pady=5)
    tk.Button(
        client_frame,
        text="Fetch Files",
        command=fetch_files,
        width=20,
        bg="#2196F3",
        fg="white",
    ).pack(pady=5)
    tk.Button(
        client_frame,
        text="Download Selected",
        command=download_selected,
        width=20,
        bg="#FF9800",
        fg="white",
    ).pack(pady=5)

    root.mainloop()
