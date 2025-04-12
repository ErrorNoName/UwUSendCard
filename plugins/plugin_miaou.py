import tkinter as tk

def run_plugin(cache):
    """
    Plugin qui affiche une fenêtre affichant "Miaou UwU".
    """
    window = tk.Toplevel()
    window.title("Plugin Miaou")
    window.geometry("200x100")
    label = tk.Label(window, text="Miaou UwU", font=("Helvetica", 16))
    label.pack(expand=True)
