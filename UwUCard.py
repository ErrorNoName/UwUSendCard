import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import requests
from io import BytesIO
import random

# --- Fonctions liées à l'animation du GIF ---
def animate_gif(frames, label, delay=100):
    def update(ind):
        label.config(image=frames[ind])
        ind = (ind + 1) % len(frames)
        root.after(delay, update, ind)
    update(0)

# --- Fonction de soumission du formulaire ---
def submit_info():
    # Récupère les informations saisies
    user_data['card'] = entry_card.get()
    user_data['expiry'] = entry_expiry.get()
    user_data['cvv'] = entry_cvv.get()
    # Transition vers l'écran de traitement
    frame_entry.pack_forget()
    show_processing_frame()

# --- Simulation du traitement avec barre de progression et messages ---
def simulate_processing(progress=0):
    # Liste de messages humoristiques en fonction de l'avancement
    messages = [
        "H-hacking in progress...",
        "C-calculating cute factor...",
        "P-probing your secrets...",
        "Encrypting adorableness...",
        "Reticulating splines... (UwU)",
        "Almost done, nya~"
    ]
    # Mise à jour de la barre de progression
    progress_var.set(progress)
    # Choisir un message en fonction de l'avancement (simple interpolation)
    msg_index = min(len(messages)-1, progress // 20)
    proc_label.config(text=messages[msg_index])
    
    if progress < 100:
        # Augmenter la progression d'une valeur aléatoire pour plus de réalisme
        next_progress = progress + random.randint(5, 15)
        if next_progress > 100:
            next_progress = 100
        root.after(300, simulate_processing, next_progress)
    else:
        # Une fois terminé, passer à l'écran final
        frame_processing.pack_forget()
        show_final_frame()

# --- Affichage de l'écran de traitement ---
def show_processing_frame():
    frame_processing.pack(fill="both", expand=True)
    simulate_processing(0)

# --- Affichage de l'écran final avec dialogue interactif ---
def show_final_frame():
    frame_final.pack(fill="both", expand=True)
    # Messages de dialogue simulé en stutter
    dialogues = [
        "UwU, th-thanks for your info...",
        "Y-y-your data is now securely backed up in the interwebs!",
        "H-hum, it's so cute how you shared it, nya~",
        "Calculating your ultimate cute factor...",
        "All done! Stay adorable!"
    ]
    
    # Affiche les dialogues un par un avec un délai
    def display_dialogues(i=0):
        if i < len(dialogues):
            final_msg_label.config(text=dialogues[i])
            root.after(1500, display_dialogues, i+1)
        else:
            # Une fois tous les messages affichés, proposer de quitter ou redémarrer
            restart_button.pack(pady=10)
            exit_button.pack(pady=10)
            
    display_dialogues()

def restart_app():
    # Réinitialise l'interface pour simuler un nouveau départ
    user_data.clear()
    # Vider les champs d'entrée
    entry_card.delete(0, tk.END)
    entry_expiry.delete(0, tk.END)
    entry_cvv.delete(0, tk.END)
    frame_final.pack_forget()
    restart_button.pack_forget()
    exit_button.pack_forget()
    frame_entry.pack(fill="both", expand=True)

# --- Configuration principale de la fenêtre ---
root = tk.Tk()
root.title("Totally Not Malware")
root.geometry("430x230")
root.resizable(False, False)
root.configure(bg="#f0f0ff")

user_data = {}

# --- Chargement et animation du GIF ---
gif_url = "https://media1.tenor.com/m/CdDaSnngrfcAAAAd/menace-alchemilla.gif"
frames = []
try:
    response = requests.get(gif_url)
    response.raise_for_status()
    img_data = BytesIO(response.content)
    gif = Image.open(img_data)
    # Itérer sur chaque frame et redimensionner (ex: 100x100 pixels)
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA").resize((100, 100), Image.LANCZOS)
        frames.append(ImageTk.PhotoImage(frame))
except Exception as e:
    print("Erreur lors du téléchargement ou traitement du GIF :", e)

# --- Écran d'entrée ---
frame_entry = tk.Frame(root, bg="#f0f0ff")
frame_entry.pack(fill="both", expand=True)

# Zone gauche pour le GIF
left_frame = tk.Frame(frame_entry, width=110, height=200, bg="#ffffff")
left_frame.pack(side="left", fill="y", padx=5, pady=5)
if frames:
    gif_label = tk.Label(left_frame, bg="#ffffff")
    gif_label.pack(expand=True)
    animate_gif(frames, gif_label, delay=100)
else:
    tk.Label(left_frame, text="(No Image)", bg="lightgray").pack(expand=True, fill="both")

# Zone droite pour le formulaire
right_frame = tk.Frame(frame_entry, bg="#f0f0ff")
right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
intro_label = tk.Label(right_frame, text="H-hi there...\nDo you th-think I could have your\ncredit card information, p-please?", 
                       justify="left", font=("TkDefaultFont", 9), bg="#f0f0ff")
intro_label.pack(anchor="w", pady=(0,5))

# Champs de saisie
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
submit_button.pack(anchor="e", pady=(5,0))

# --- Écran de traitement ---
frame_processing = tk.Frame(root, bg="#f0f0ff")
proc_label = tk.Label(frame_processing, text="Initializing...", font=("TkDefaultFont", 10), bg="#f0f0ff")
proc_label.pack(pady=10)
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(frame_processing, orient="horizontal", length=300, mode="determinate", variable=progress_var)
progress_bar.pack(pady=5)

# --- Écran final ---
frame_final = tk.Frame(root, bg="#f0f0ff")
final_msg_label = tk.Label(frame_final, text="", font=("TkDefaultFont", 10), bg="#f0f0ff", justify="center")
final_msg_label.pack(pady=20)
restart_button = tk.Button(frame_final, text="Restart", command=restart_app, font=("TkDefaultFont", 8))
exit_button = tk.Button(frame_final, text="Exit", command=root.quit, font=("TkDefaultFont", 8))

# Démarrage de la boucle principale
root.mainloop()
