import tkinter as tk
import _tkinter  # Forcer l'importation
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageSequence
import os, json, subprocess, threading, sys
from io import BytesIO

# Fichier de configuration et dossier des plugins
CONFIG_FILE = "config.json"
PLUGINS_DIR = "plugins"

def load_available_plugins():
    plugins = []
    if os.path.isdir(PLUGINS_DIR):
        for file in os.listdir(PLUGINS_DIR):
            if file.endswith(".py") and file != "__init__.py":
                plugins.append(file[:-3])
    return plugins

def save_config(selected_plugins):
    config = {"plugins": selected_plugins}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"plugins": []}

# --- Interface du Loader avec logs ---
class LoaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Loader de Génération - Totally Not Malware")
        self.geometry("600x600")
        self.configure(bg="#ffe6fa")
        
        self.available_plugins = load_available_plugins()
        self.plugins_vars = {}  # dict: plugin -> IntVar
        
        # Cadre supérieur : affichage du GIF animé
        self.setup_gif_panel()
        
        # Cadre central : sélection des plugins
        self.setup_plugins_panel()
        
        # Cadre inférieur : génération et logs
        self.setup_generation_panel()
        
    def setup_gif_panel(self):
        self.gif_frame = tk.Frame(self, bg="#ffe6fa")
        self.gif_frame.pack(pady=10)
        
        # Chargement du GIF en local depuis src/uwu.gif
        gif_path = os.path.join("src", "uwu.gif")
        self.gif_frames = []
        try:
            if os.path.exists(gif_path):
                gif = Image.open(gif_path)
                # Itération sur chaque frame, redimensionnement à 150x150
                for frame in ImageSequence.Iterator(gif):
                    frame = frame.convert("RGBA").resize((150, 150), Image.LANCZOS)
                    self.gif_frames.append(ImageTk.PhotoImage(frame))
            else:
                print(f"Le fichier GIF n'a pas été trouvé : {gif_path}")
        except Exception as e:
            print("Erreur lors de l'ouverture ou du traitement du GIF :", e)
            
        if self.gif_frames:
            self.gif_label = tk.Label(self.gif_frame, bg="#ffe6fa")
            self.gif_label.pack()
            self.animate_gif(0)
        else:
            tk.Label(self.gif_frame, text="(No Image)", bg="lightgray").pack()
    
    def animate_gif(self, index, delay=100):
        self.gif_label.config(image=self.gif_frames[index])
        next_index = (index + 1) % len(self.gif_frames)
        self.after(delay, self.animate_gif, next_index, delay)
    
    def setup_plugins_panel(self):
        self.plugins_frame = tk.LabelFrame(self, text="Sélection des Plugins", bg="#ffe6fa", font=("Segoe UI", 12, "bold"), fg="#d63384")
        self.plugins_frame.pack(padx=20, pady=10, fill="both", expand=False)
        
        self.plugins_vars = {}
        # Liste des plugins sous forme de cases à cocher
        for plugin in self.available_plugins:
            var = tk.IntVar()
            chk = tk.Checkbutton(self.plugins_frame, text=plugin, variable=var, bg="#ffe6fa", font=("Segoe UI", 10))
            chk.pack(anchor="w", pady=2, padx=10)
            self.plugins_vars[plugin] = var
        
        # Bouton pour sauvegarder la configuration
        self.btn_save_config = tk.Button(self.plugins_frame, text="Sauvegarder Config", command=self.save_config_action, font=("Segoe UI", 10, "bold"), bg="#d63384", fg="white")
        self.btn_save_config.pack(pady=10)
    
    def save_config_action(self):
        selected = [name for name, var in self.plugins_vars.items() if var.get() == 1]
        save_config(selected)
        messagebox.showinfo("Config", "Configuration sauvegardée !")
    
    def setup_generation_panel(self):
        self.generation_frame = tk.Frame(self, bg="#ffe6fa")
        self.generation_frame.pack(pady=10, fill="both", expand=True)
        
        # Bouton pour générer l'exécutable
        self.btn_generate = tk.Button(self.generation_frame, text="Générer .exe", command=self.start_generation, font=("Segoe UI", 12, "bold"), bg="#198754", fg="white")
        self.btn_generate.pack(pady=5)
        
        # Barre de progression indéterminée
        self.progress = ttk.Progressbar(self.generation_frame, orient="horizontal", mode="indeterminate")
        self.progress.pack(pady=5, padx=20, fill="x")
        
        # Zone de log pour afficher la sortie de PyInstaller
        self.log_text = scrolledtext.ScrolledText(self.generation_frame, height=10, state="disabled", bg="#f8f9fa", fg="black", font=("Consolas", 9))
        self.log_text.pack(pady=10, padx=10, fill="both", expand=True)
    
    def log(self, message):
        """Ajoute un message dans la zone de log."""
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")
    
    def start_generation(self):
        self.btn_generate.config(state="disabled")
        self.btn_save_config.config(state="disabled")
        for widget in self.plugins_frame.winfo_children():
            if isinstance(widget, tk.Checkbutton):
                widget.config(state="disabled")
        
        self.log("=== Lancement de la génération ===")
        self.progress.start(10)
        threading.Thread(target=self.generate_exe, daemon=True).start()
    
    def generate_exe(self):
        selected = [name for name, var in self.plugins_vars.items() if var.get() == 1]
        save_config(selected)
        
        # Préparation des arguments pour inclure plugins et src, et ajouter le hidden import pour PIL._tkinter_finder
        add_data_plugins = "plugins;plugins" if os.name == "nt" else "plugins:plugins"
        add_data_src = "src;src" if os.name == "nt" else "src:src"
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--hidden-import", "PIL._tkinter_finder",  # Ajout du hidden import
            "--add-data", add_data_plugins,
            "--add-data", add_data_src,
            "main.py"
        ]
        
        self.log("Commande : " + " ".join(cmd))
        self.log("Démarrage de PyInstaller...")
        
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in proc.stdout:
                self.log(line.rstrip())
            proc.wait()
            result = proc.returncode
        except Exception as e:
            result = 1
            self.log("Exception lors de la génération : " + str(e))
        
        self.after(0, self.generation_finished, result)
    
    def generation_finished(self, result):
        self.progress.stop()
        self.btn_generate.config(state="normal")
        self.btn_save_config.config(state="normal")
        for widget in self.plugins_frame.winfo_children():
            if isinstance(widget, tk.Checkbutton):
                widget.config(state="normal")
        
        if result == 0:
            self.log("Génération terminée avec succès !")
            messagebox.showinfo("Succès", "Génération terminée !")
            if messagebox.askyesno("Lancer ?", "Voulez-vous lancer l'application générée ?"):
                self.launch_generated_app()
        else:
            self.log("La génération a échoué. Voir les logs ci-dessus.")
            messagebox.showerror("Erreur", "La génération a échoué. Consultez la zone de log pour plus de détails.")
    
    def launch_generated_app(self):
        exe_path = os.path.join("dist", "main.exe") if os.name == "nt" else os.path.join("dist", "main")
        if os.path.exists(exe_path):
            self.log("Lancement de l'application générée...")
            try:
                subprocess.Popen([exe_path])
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lancer l'app : {e}")
        else:
            messagebox.showerror("Erreur", "L'exécutable n'a pas été trouvé.")

if __name__ == "__main__":
    app = LoaderApp()
    app.mainloop()
