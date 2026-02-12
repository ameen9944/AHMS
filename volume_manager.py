import tkinter as tk
from tkinter import ttk
import subprocess
import sys

def get_volume():
    try:
        result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], capture_output=True, text=True)
        return int(result.stdout.strip())
    except:
        return 50  # default

def set_volume(volume):
    try:
        subprocess.run(['osascript', '-e', f'set volume output volume {volume}'])
    except:
        pass

def get_muted():
    try:
        result = subprocess.run(['osascript', '-e', 'output muted of (get volume settings)'], capture_output=True, text=True)
        return result.stdout.strip() == 'true'
    except:
        return False

def set_muted(muted):
    try:
        subprocess.run(['osascript', '-e', f'set volume output muted {muted}'])
    except:
        pass

class VolumeManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Volumi App")
        self.root.geometry("400x300")

        self.volume = tk.IntVar(value=get_volume())
        self.muted = tk.BooleanVar(value=get_muted())

        ttk.Label(root, text="Volume Generale:").pack(pady=10)
        self.volume_slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', variable=self.volume, command=self.update_volume)
        self.volume_slider.pack(fill='x', padx=20)

        self.mute_button = ttk.Checkbutton(root, text="Muto", variable=self.muted, command=self.toggle_mute)
        self.mute_button.pack(pady=10)

        # For apps, since macOS doesn't have per-app volume easily, we'll simulate with sliders for different apps
        ttk.Label(root, text="Volumi App:").pack(pady=10)

        self.app_volumes = {}
        apps = ["Chrome", "Safari", "Spotify", "VLC"]  # example apps
        for app in apps:
            frame = ttk.Frame(root)
            frame.pack(fill='x', padx=20, pady=5)
            ttk.Label(frame, text=f"{app}:").pack(side='left')
            slider = ttk.Scale(frame, from_=0, to=100, orient='horizontal')
            slider.pack(side='right', fill='x', expand=True)
            self.app_volumes[app] = slider

        ttk.Button(root, text="Applica", command=self.apply_app_volumes).pack(pady=10)

    def update_volume(self, value):
        set_volume(int(float(value)))

    def toggle_mute(self):
        set_muted(self.muted.get())

    def apply_app_volumes(self):
        # Since per-app volume is not directly supported, we'll just print or simulate
        for app, slider in self.app_volumes.items():
            vol = slider.get()
            print(f"Imposta volume per {app} a {vol}%")
            # In real implementation, you'd need to use AppleScript or other methods to control app volumes

if __name__ == "__main__":
    root = tk.Tk()
    app = VolumeManager(root)
    root.mainloop()
