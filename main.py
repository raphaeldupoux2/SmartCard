import tkinter as tk
from tkinter import messagebox
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.pcsc.PCSCReader import PCSCReader


class SmartCardReaderApp:
    """
    Une application de lecteur de carte intelligente.

    Cette application crée une interface graphique pour un lecteur de carte
    intelligent. Il permet de sélectionner un lecteur externe et de lire une
    carte pour afficher les informations.

    Args:
        master: Fenêtre principale de l'application.

    Attributes:
        master (tk.Tk): Fenêtre principale de l'application.
        isen_logo (tk.PhotoImage): Logo de l'ISEN affiché dans l'interface.
        logo_label (tk.Label): Widget d'étiquette pour afficher le logo de l'ISEN.
        select_reader_menu (tk.OptionMenu): Menu déroulant pour sélectionner le lecteur externe.
        read_card_button (tk.Button): Bouton pour lire la carte.
        info_text (tk.Text): Zone de texte pour afficher les informations de la carte.

    """

    def __init__(self, master):
        """
        Initialise l'application de lecteur de carte intelligente.

        Args:
            master (tk.Tk): Fenêtre principale de l'application.
        """
        self.master = master
        master.title("SmartCard Reader ISEN")
        master.geometry("1400x800")

        # Chargement du logo de l'ISEN
        #self.isen_logo = tk.PhotoImage(file="isen_logo.png")
        #self.isen_logo_resized = self.isen_logo.subsample(2, 2)  # Réduction de moitié
        #self.logo_label = tk.Label(master, image=self.isen_logo_resized)
        #self.logo_label.pack()

        # Menu déroulant pour sélectionner le lecteur externe
        self.reader_selection = tk.StringVar(master)
        self.reader_selection.set("Sélectionner lecteur externe")
        self.readers = readers()
        self.select_reader_menu = tk.OptionMenu(master, self.reader_selection, *self.readers,
                                                command=self.update_card_reader)
        self.select_reader_menu.pack()

        # Zone de texte pour afficher les informations renvoyées par la carte
        self.info_text = tk.Text(master, height=30, width=165)
        self.info_text.pack()

        # Bouton pour lire la carte
        self.read_card_button = tk.Button(master, text="Lire la carte", command=self.read_card)
        self.read_card_button.pack()

        # Initialisation du lecteur
        self.card_reader = None

    def update_card_reader(self, selected_reader):
        """
        Met à jour l'objet lecteur avec le lecteur sélectionné.

        Args:
            selected_reader (str): Nom du lecteur sélectionné.
        """
        self.card_reader = PCSCReader(selected_reader)

    def read_card(self):
        """
        Lit les informations de la carte.

        Affiche les informations de la carte lue dans la zone de texte.
        """
        if self.card_reader is None:
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner un lecteur externe.")
            return

        try:
            card_connection = self.card_reader.createConnection()
            card_connection.connect()
            atr = toHexString(card_connection.getATR())
            card_info = f"Informations de la carte lue...\nATR: {atr}\n"
            self.info_text.insert(tk.END, card_info)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture de la carte : {str(e)}")


# Création de la fenêtre principale
root = tk.Tk()
app = SmartCardReaderApp(root)

# Lancement de la boucle principale de la fenêtre
root.mainloop()