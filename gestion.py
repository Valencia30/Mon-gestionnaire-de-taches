import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QLineEdit, QMessageBox, QInputDialog, QListWidgetItem , QGroupBox
from PySide6.QtGui import QColor, Qt

class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mon gestionnaire de tâches")
        self.setGeometry(100, 100, 300, 400)
        

        self.taches = []
        self.setup_ui()
        self.charger_taches()
    
    def setup_ui(self):

        layout_principal = QVBoxLayout()
        # Création du QGroupBox
        group_box = QGroupBox("Gestionnaire de tâches")
        layout_principal.addWidget(group_box)
        
        layout_group_box = QVBoxLayout(group_box)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrer le layout
        layout.setContentsMargins(450, 0, 450, 0)
        
        # Création d'un widget pour contenir les boutons "Ajouter" et "Supprimer"
        widget_boutons = QWidget()
        layout.addWidget(widget_boutons)

        layout_boutons = QVBoxLayout(widget_boutons)
        

        # Bouton "Ajouter" en haut à droite
        bouton_ajouter = QPushButton("Ajouter une tâche")
        bouton_ajouter.clicked.connect(self.ajouter_tache)
        layout_boutons.addWidget(bouton_ajouter, alignment=Qt.AlignmentFlag.AlignRight)  # Utilisation de Qt.AlignmentFlag

        # Bouton "Supprimer" en bas
        bouton_supprimer = QPushButton("Supprimer la tâche sélectionnée")
        bouton_supprimer.clicked.connect(self.supprimer_tache)
        layout_boutons.addWidget(bouton_supprimer)

        # Liste des tâches
        self.liste_taches = QListWidget()
        layout.addWidget(self.liste_taches)
        
        # Ajout de la saisie de tâche
        self.saisie_tache = QLineEdit()
        layout.addWidget(self.saisie_tache)
        
        # Boutons "Modifier" en bas à gauche
        layout_boutons_modifier = QVBoxLayout()
        bouton_modifier_tache = QPushButton("Modifier la tâche sélectionnée")
        bouton_modifier_tache.clicked.connect(self.modifier_taches)
        layout_boutons_modifier.addWidget(bouton_modifier_tache)

        bouton_modifier_etat = QPushButton("Modifier l'état de la tâche sélectionnée")
        bouton_modifier_etat.clicked.connect(self.modifier_etat_tache)
        layout_boutons_modifier.addWidget(bouton_modifier_etat)

        layout.addLayout(layout_boutons_modifier)

        # Bouton "Enregistrer" en bas à droite
        bouton_enregistrer = QPushButton("Enregistrer les tâches")
        bouton_enregistrer.clicked.connect(self.enregistrer_taches)
        layout.addWidget(bouton_enregistrer, alignment=Qt.AlignmentFlag.AlignRight)  # Utilisation de Qt.AlignmentFlag

        widget_central = QWidget()
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)

    def ajouter_tache(self):
        texte_tache = self.saisie_tache.text()
        if texte_tache:
            self.taches.append({"tache": texte_tache, "etat": "en attente"})
            self.actualiser_liste_taches()
            self.saisie_tache.clear()
    
    def supprimer_tache(self):
        if self.liste_taches.currentRow() != -1:
            del self.taches[self.liste_taches.currentRow()]
            self.actualiser_liste_taches()
    
    def modifier_etat_tache(self):
        if self.liste_taches.currentRow() != -1:
            index_tache = self.liste_taches.currentRow()
            tache_actuelle = self.taches[index_tache]
            options = ["en attente", "en cours", "terminé"]
            option, ok = QInputDialog.getItem(self, "Modifier l'état de la tâche", "Sélectionnez un nouvel état :", options, options.index(tache_actuelle["etat"]), False)
            if ok:
                self.taches[index_tache]["etat"] = option
                self.actualiser_liste_taches()

    def modifier_taches(self):
        if self.liste_taches.currentRow() != -1:
            nouveau_texte_tache, ok = QInputDialog.getText(self, "Modifier la tâche", "Entrez la nouvelle tâche :", QLineEdit.Normal, self.taches[self.liste_taches.currentRow()]["tache"])
            if ok and nouveau_texte_tache:
                self.taches[self.liste_taches.currentRow()]["tache"] = nouveau_texte_tache
                self.actualiser_liste_taches()

    def enregistrer_taches(self):
        try:
            with open("taches.txt", "w") as fichier:
                for tache in self.taches:
                    fichier.write(f"{tache['tache']}|{tache['etat']}\n")
            QMessageBox.information(self, "Enregistrement", "Les tâches ont été enregistrées avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'enregistrement : {str(e)}")
    
    def charger_taches(self):
        try:
            with open("taches.txt", "r") as fichier:
                for ligne in fichier:
                    tache, etat = ligne.strip().split("|")
                    self.taches.append({"tache": tache, "etat": etat})
        except FileNotFoundError:
            pass
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors du chargement des tâches : {str(e)}")
    
    def actualiser_liste_taches(self):
        self.liste_taches.clear()
        for tache in self.taches:
            item = QListWidgetItem(f"{tache['tache']} ({tache['etat']})")
            if tache['etat'] == 'en cours':
                item.setBackground(QColor('blue'))
            elif tache['etat'] == 'terminé':
                item.setBackground(QColor('green'))
            else:
                item.setBackground(QColor('red'))
            self.liste_taches.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    fenetre.show()
    sys.exit(app.exec())
