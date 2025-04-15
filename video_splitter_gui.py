import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

class VideoSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Splitter - Yo, Chop It Up! 😎")
        self.root.geometry("600x500")
        
        # FFmpeg path input
        tk.Label(root, text="FFmpeg Path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.ffmpeg_entry = tk.Entry(root, width=50)
        self.ffmpeg_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_ffmpeg).grid(row=0, column=2, padx=10)
        
        # Input video path
        tk.Label(root, text="Input Video Path:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_input).grid(row=1, column=2, padx=10)
        
        # Output folder
        tk.Label(root, text="Output Folder:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.output_entry = tk.Entry(root, width=50)
        self.output_entry.grid(row=2, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_output).grid(row=2, column=2, padx=10)
        
        # Segment duration
        tk.Label(root, text="Split Every (seconds):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.time_entry = tk.Entry(root, width=10)
        self.time_entry.insert(0, "60")
        self.time_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Total duration to process
        tk.Label(root, text="Process Up To (minutes, min 1):").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.duration_entry = tk.Entry(root, width=10)
        self.duration_entry.insert(0, "1")
        self.duration_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        # Output name
        tk.Label(root, text="Output Name (e.g., clip):").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = tk.Entry(root, width=20)
        self.name_entry.insert(0, "output")
        self.name_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        
        # Run Button
        tk.Button(root, text="Chop It!", command=self.run_split, bg="green", fg="white").grid(row=6, column=1, pady=20)
    
    def browse_ffmpeg(self):
        file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe"), ("All files", "*.*")])
        if file_path:
            self.ffmpeg_entry.delete(0, tk.END)
            self.ffmpeg_entry.insert(0, file_path)
    
    def browse_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi")])
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
    
    def browse_output(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder_path)
    
    def run_split(self):
        ffmpeg_path = self.ffmpeg_entry.get()
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()
        segment_time = self.time_entry.get()
        duration = self.duration_entry.get()
        output_name = self.name_entry.get()
        
        # Validate inputs
        if not os.path.exists(ffmpeg_path) or not ffmpeg_path.endswith("ffmpeg.exe"):
            messagebox.showerror("Error", "Yo, that FFmpeg path ain't legit! Find ffmpeg.exe. 😕")
            return
        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Yo, that video file ain't real! 😕")
            return
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except:
                messagebox.showerror("Error", "Can't make that output folder, fam! 😤")
                return
        if not segment_time.isdigit() or int(segment_time) <= 0:
            messagebox.showerror("Error", "Gimme a real number for split time, yo! 😒")
            return
        if not duration.replace(".", "").isdigit() or float(duration) < 1:
            messagebox.showerror("Error", "Duration gotta be at least 1 minute, fam! 😒")
            return
        if not output_name:
            output_name = "output"
        
        # Convert duration to seconds
        duration_seconds = int(float(duration) * 60)
        
        # Build FFmpeg command
        output_pattern = os.path.join(output_path, f"{output_name}_%03d.mp4")
        cmd = [
            ffmpeg_path,
            "-i", input_path,
            "-t", str(duration_seconds),
            "-f", "segment",
            "-segment_time", segment_time,
            "-c", "copy",
            output_pattern
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            messagebox.showinfo("Success", "Yo, vids chopped up clean in the folder! 😎")
        except FileNotFoundError:
            messagebox.showerror("Error", "FFmpeg ain't where you said, fam! Check the path. 😖")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Damn, somethin' broke: {e.stderr} 😵")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoSplitterGUI(root)
    root.mainloop()