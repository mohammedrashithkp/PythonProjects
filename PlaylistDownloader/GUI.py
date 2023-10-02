from pytube import Playlist, YouTube
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import os
import threading

def download_video(url, output_path, progress_bar, playlist_name):
    def on_progress(stream, chunk, remaining_bytes):
        total_size = stream.filesize
        bytes_downloaded = total_size - remaining_bytes
        progress = int(bytes_downloaded / total_size * 100)
        progress_bar["value"] = progress
        root.update_idletasks()

    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.get_highest_resolution()
    output_directory = os.path.join(output_path, playlist_name)  # Create a directory with playlist name
    os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
    output_file = os.path.join(output_directory, f"{yt.title}.mp4")

    if not os.path.exists(output_file):
        stream.download(output_path=output_directory)
        show_notification("Download Complete", f"{yt.title} downloaded successfully!")
    else:
        show_notification("Skipped", f"{yt.title} already exists, skipping...")

def show_notification(title, message):
    root.bell()  # Beep to notify user
    messagebox.showinfo(title, message)

def open_url():
    url = playlist_url.get()
    try:
        if url:
            playlist = Playlist(url)
            resolution = "720p"

            # Get user-selected output directory
            output_path = selected_directory.get()

            for video_url in playlist.video_urls:
                # Get the playlist name for folder creation
                playlist_name = playlist.title()
                download_video(video_url, output_path, progress_bar, playlist_name)
            
            show_notification("Playlist Download Complete", "Playlist download completed!")
        else:
            show_notification("Error", "Please enter a URL. ")

    except Exception as e:
        show_notification("Error", f"Error: {e}")

def choose_output_directory():
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        selected_directory.set(selected_dir)

root = tk.Tk()
root.title("PlaylistDownloader")
root.configure(bg="lightgray")

label = tk.Label(root, text="Enter a URL:", bg="lightgray")
label.pack(pady=10)

playlist_url = tk.Entry(root, width=40)
playlist_url.pack(pady=5)

choose_directory_button = tk.Button(root, text="Choose Download Directory", command=choose_output_directory, bg="lightblue")
choose_directory_button.pack(pady=5)

selected_directory = tk.StringVar()
output_directory_label = tk.Label(root, textvariable=selected_directory, bg="lightgray")
output_directory_label.pack(pady=5)

submit_button = tk.Button(root, text="Submit", command=open_url, bg="green", fg="white")
submit_button.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=200, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()
