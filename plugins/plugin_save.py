import json

def run_plugin(cache):
    """
    Plugin qui sauvegarde le cache dans data.json.
    """
    try:
        with open("data.json", "w") as f:
            json.dump(cache, f, indent=4)
        print("Data saved to data.json")
    except Exception as e:
        print("Erreur lors de la sauvegarde :", e)
