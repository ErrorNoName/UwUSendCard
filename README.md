# UwUSendCard - Totally Not Malware (Kawaii Egirl Edition)

![Egirl](https://media1.tenor.com/m/CdDaSnngrfcAAAAd/menace-alchemilla.gif)

Bienvenue dans **UwUSendCard** – une application ultra-mignonne (kawaii !) qui se présente comme un faux logiciel de collecte de données, mais qui sert en réalité de base modulable et amusante pour expérimenter des plugins et créer vos propres comportements après la collecte d'informations.  
*Ne vous inquiétez pas, c'est totalement fake et fait pour rire !*
*Sauf si vous décidez d'en créer un malware à l'aide des plugins send webhook, tokengrab etc..*

---

## Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Création de Plugins](#création-de-plugins)
- [Le Loader et la Génération](#le-loader-et-la-génération)
- [Compilation](#compilation)
- [Licence](#licence)

---

## Aperçu

UwUSendCard est une application Python avec interface graphique (Tkinter) qui simule la collecte d’informations sensibles. Le but est de montrer comment développer une base extensible avec un **système de plugins**. Chaque plugin peut réaliser une action complémentaire après la saisie des données (par exemple, sauvegarder les données dans un fichier JSON, afficher un message mignon comme "Miaou UwU", etc.).

---

## Fonctionnalités

- **Interface Kawaii Egirl !**  
  Une interface rétro et adorable qui demande les informations (numéro de carte, date d’expiration, code de sécurité).
  
- **Système de Plugins Modulaire**  
  Extensible via des plugins placés dans le dossier `plugins`. Chaque plugin est un module Python qui définit une fonction `run_plugin(cache)` pour traiter les données saisies.
  
- **Loader de Génération**  
  Un panneau de configuration (loader) vous permet de choisir les plugins à intégrer puis de générer un exécutable (.exe ou équivalent) avec PyInstaller. Vous pouvez suivre l’évolution de la compilation à travers une zone de logs en temps réel.

- **Compilation Automatisée**  
  Le loader intègre la génération de l’exécutable, incluant les ressources telles que le GIF (dans le dossier `src`) et les plugins sélectionnés.

---

## Installation

1. **Cloner le dépôt**  
   ```bash
   git clone https://votre-url-depot.git
   cd UwUSendCard
   ```

2. **Créer un environnement virtuel** (optionnel mais recommandé)  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Installer les dépendances**  
   ```bash
   pip install -r requirements.txt
   ```  
   *Les packages requis sont Tkinter (inclus avec Python), Pillow, et PyInstaller.*

---

## Utilisation

- **Exécution de l'application principale :**  
  Lancez le script `main.py` pour tester l'application en mode démo.  
  ```bash
  python main.py
  ```

- **Utilisation du Loader :**  
  Lancez `loader.py` pour configurer les plugins à intégrer dans votre exécutable et générer le fichier compilé.
  ```bash
  python loader.py
  ```

---

## Création de Plugins

Les plugins se trouvent dans le dossier `plugins`.  
Chaque plugin doit être un fichier Python (ex : `plugin_save.py`, `plugin_miaou.py`) et doit définir une fonction :

```python
def run_plugin(cache):
    """
    Cette fonction reçoit le cache des données saisies et effectue une action.
    Par exemple :
      - Sauvegarder les données dans un fichier JSON.
      - Afficher une fenêtre avec un message "Miaou UwU".
    """
    # Votre code ici
```

### Exemple de plugin

Un plugin simple pour sauvegarder les données :

```python
import json

def run_plugin(cache):
    # Sauvegarde les données dans data.json
    with open("data.json", "w") as f:
        json.dump(cache, f, indent=4)
    print("Données sauvegardées dans data.json")
```

Vous pouvez créer autant de plugins que vous le souhaitez et les placer dans le dossier `plugins`.

---

## Le Loader et la Génération

Le **Loader** (script `loader.py`) est un panneau de configuration graphique qui permet de :

2. **Sélectionner les plugins** via des cases à cocher dans une interface soignée.
3. **Sauvegarder la configuration** qui liste les plugins à utiliser.
4. **Générer l’exécutable final** en appelant PyInstaller, avec une barre de progression et une zone de logs qui affiche les informations de compilation en temps réel.

Une fois l’exécutable généré, le loader vous propose de lancer directement l’application compilée.

---

## Compilation

Pour compiler l’application en un exécutable autonome, le loader exécute PyInstaller avec les options nécessaires.  
**Important :**

- Le dossier `src` (contenant le GIF `uwu.gif`) et le dossier `plugins` sont inclus dans la compilation.
- Utilisez la commande suivante (le loader le fait automatiquement) :

Pour **Windows** :
```bash
pyinstaller --onefile --windowed --hidden-import PIL._tkinter_finder --add-data "plugins;plugins" --add-data "src;src" main.py
```

Pour **Linux/Mac** :
```bash
pyinstaller --onefile --windowed --hidden-import PIL._tkinter_finder --add-data "plugins:plugins" --add-data "src:src" main.py
```

Assurez-vous que votre environnement est bien configuré et que toutes les dépendances sont installées.

---

## Licence

Ce projet est fourni à titre éducatif. Utilisez-le et modifiez-le à votre guise pour vos projets personnels ou éducatifs.  
*UwU, restez adorables et prudents !*
