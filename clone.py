import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import vlc
import os

# Sample movie data (replace with your own video paths and thumbnails)
movies = [
    {"title": "Movie 1", "file": "videos/movie1.mp4", "thumbnail": "thumbnails/movie1.jpg"},
    {"title": "Movie 2", "file": "videos/movie2.mp4", "thumbnail": "thumbnails/movie2.jpg"},
    {"title": "Movie 3", "file": "videos/movie3.mp4", "thumbnail": "thumbnails/movie3.jpg"},
]

class NetflixCloneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Netflix Clone")
        self.root.geometry("800x600")
        self.player = None

        self.create_ui()

    def create_ui(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        for movie in movies:
            self.add_movie_card(movie)

    def add_movie_card(self, movie):
        frame = ttk.Frame(self.scrollable_frame, padding=10)
        frame.pack(pady=5, fill="x")

        try:
            img = Image.open(movie["thumbnail"])
            img = img.resize((120, 70))
            photo = ImageTk.PhotoImage(img)
        except:
            photo = None

        label = ttk.Label(frame, image=photo)
        label.image = photo
        label.pack(side="left")

        title = ttk.Label(frame, text=movie["title"], font=("Arial", 14))
        title.pack(side="left", padx=10)

        play_button = ttk.Button(frame, text="Play", command=lambda: self.play_movie(movie["file"]))
        play_button.pack(side="right")

    def play_movie(self, path):
        if not os.path.exists(path):
            tk.messagebox.showerror("Error", f"File not found: {path}")
            return

        if self.player:
            self.player.stop()

        instance = vlc.Instance()
        self.player = instance.media_player_new()
        media = instance.media_new(path)
        self.player.set_media(media)
        self.player.play()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = NetflixCloneApp(root)
    root.mainloop()
