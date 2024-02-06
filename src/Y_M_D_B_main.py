#!/usr/bin/env python3

import random
import re 
import argparse
import tkinter as tk
#On va commencer par créer une class pour les cases
class Demineur_case:
    # ensuite integrer un constructeur
    def _init_(self):
        self.valeur = 0
        self.mine = False
        self.decouverte = False

    def get_valeur(self):
        return self.valeur

    def get_mine(self):
        return self.mine

    def get_decouverte(self):
        return self.decouverte

    def set_valeur(self, valeur ):
        self.valeur = valeur

    def set_mine(self, mine):
        self.mine = mine
    
    def set_decouverte(self,decouverte):
        self.decouverte = decouverte 

    def _str_(self):
        return str(str.valeur)

#créer une classe pour les griles de notre jeu
class Demineur_grille:
    #integrer un construction qui va initialiser les grilles
    def _init_(self, taille, nbre_bombes): 
        self.taille = taille
        self.nbre_bombes = nbre_bombes
        #intronisation du tableaau du demnineur (demineur_case)
        self.plateau = [[Demineur_case() for i in range(taille)] for j in range(taille)]# j'ai créer une boucle imbriqué afin de créer un plateau en fonction de la taille de nos cases
        #intronisation des cases jouables soient des cases sans mines
        self.cases_jouables = taille * taille - nbre_bombes 
        compteur_bombes = 0
        while compteur_bombes < nbre_bombes : # cette conditon va nous permettre de placer correctement les bombes
            x = random.randint(0, self.taille - 1) # avec random nous pourrons obtenir des coordonnée de x aléatoirement
            y = random.randint(0, self.taille - 1) # avec random nous pourrons obtenir des coordonnée de y aléatoirement
            if not self.plateau[x][y].get_mine():
                compteur_bombes = compteur_bombes + 1
                self.place_bombes(x, y) #placement des bombes en fonction de x et y

    def get_cases_joouables(self):
        return self.cases_jouables
     # nous allons placer de manière adjacente les valeurs de cases avec la fonction place_bombes
    def place_bombes(self, x, y):
        self.plateau[x][y].set_mine(True)
        for j in range(x-1, x+2):
            #vérifions si la case est dans notre grille
            for i in range(y-1, y+2):
                if j >= 0 and i >= 0 and j < self.taille and i < self.taille:
                    self.plateau[j][i].set_valeur(self.plateau[j][i].get_valeur()+1)
    #affichons notre grille sur notre console
    def _str_(self):
        grille = ' '
        for j in range(self.taille):
            if j < 10:
                grille = grille + ' ' * 2 + str(j) + ' ' * 2 
            else: 
                grille = grille + ' ' + str(j) + ' ' * 2
        grille = grille + '\n' #le back slash sert a faire un retour a la ligne
        for j in range(self.taille):
            grille +=  '-' * 5 
            if j == self.taille - 1:
                grille += '--' + '\n' #cela va servir a faire un retour a la ligne avec des pointillet
        for j in range(self.taille):
            if j < 10 : 
                #nous allons ajouter la première colonne
                grille += str(j) + ' | '
            else:
                grille += str(j) + ' | '
            for i in range(self.taille):
                if self.plateau[j][i].get_decouverte():
                    if self.plateau[j][i].get_mine():
                        grille += "* |  "
                    else:
                        grille += str(self.plateau[j][i].get_valeur()) + ' |  '
                else:
                    grille += '  |  '
            grille += "\n"
            for j in range(self.taille):
                grille += '-' * 5
                if j == self.taille - 1:
                    grille += '--' + "\n"
            return grille
    def decouverte_case(self, x, y):#cases que notre joueur desire d'entrées
        self.cases_jouables = self.cases_jouables - 1 
        self.plateau[x][y].set_decouverte(True)
        if self.plateau[x][y].get_mine():
            return False
        else:
            if self.plateau[x][y].get_valeur() == 0:
                for j in range(x-1, x+2):
                    for i in range(y-1, y+2):
                        if (j >= 0 and i >= 0 and 
                                j < self.taille and 
                                i < self.taille and 
                                not (j == x and i == y) and 
                                not self.plateau[j][i].get_decouverte()):
                            self.decouverte_case(j, i)
                return True 
            else: 
                return True

class Demineur_jeu:
    # voici la classe représentante de notre partie du démineur
    def _init_(self, taille, bombe): # ceci est notre contructeur
         self.taille = taille
         self.bombe = bombe
         self.grille = Demineur_grille(taille, bombe)
         self.victoire = False
         self.defaite = False

    def demande_joueur(self):# demande les coordonnées que le joueur souhaite
        saisie_valide = False
        saisie = input("Où souhaitez-vous jouer ? Entrer ligne colonne : ")
        saisie_analyse = re.match(r"^\s*(?P<x>\d+)\s*,\s*(?P<y>\d+)\s*$", saisie)
        if saisie_analyse:
            x = int(saisie_analyse.group("x"))
            y = int(saisie_analyse.group("y"))
            if x >= self.taille:
                print("x trop grand")
                saisie_valide = False 
            if y >= self.taille:
                print("y trop grand")
                saisie_valide = False
            if self.grille.plateau[x][y].get_decouverte() == True:
                print("Cette case a déjà été decouverte")
                saisie_valide = False
        else:
            print("Les coordonnées ne sont pas exactes.")
            saisie_valide = False
        return x, y
    
    def lancer_jeu(self):
        while not (self.victoire or self.defaite):
            print(self.grille)
            x, y = self.demande_joueur()
            self.defaite = not self.grille.decouverte_case(x, y)
            if self.grille.cases_jouables == 0:
                self.victoire = True
        if self.defaite:
            print("Game Over")
        if self.victoire:
            print(" Quelle jeune victoire aberrante")
        for j in range(0, self.taille):
            for i in range(0, self.taille):
                self.grille.plateau[j][i].set_decouverte(True)
        print(self.grille)

    def menu():
        parser = argparse.ArgumentParser(description = "Bienvenue sur le jeu du Démineur")
        parser.add_argument("-s", "--size", aide = "Taille du tableau", default = 16)
        parser.add_argument("-b", "--bomb", aide = "Nombre de bombes", default = 16)
        args = parser.parse_args()
        return vars(args)
    
    if "_name_" == "_main_":
        rejouer = True
        parametres = menu()
        p_taille = int(parametres["size"])
        p_bombe = int(parametres["bomb"])
        if p_taille**2 <= p_bombe:
            raise ArithmeticError("le nombre de bombe est superieur a la limite")
        while rejouer:
            jeu = Demineur_case(p_taille, p_bombe)
            jeu.lancer_jeu()
            replay = input("Désirez-vous refaire une partie ? (oui/non)")
            if re.match("^[o|O][u|U][i|I]$", replay):
                rejouer = True
            else: 
                rejouer = False
                print(" Ainsi se termine notre jeune partie ")
class DemineurGUI:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0] * cols for _ in range(rows)]
        self.generate_mines()
        self.create_widgets()

    def generate_mines(self):
        mine_count = 0
        while mine_count < self.mines:
            row, col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if self.board[row][col] != -1:
                self.board[row][col] = -1
                mine_count += 1

    def create_widgets(self):
        self.buttons = [[tk.Button(self.master, width=2, height=1, command=lambda r=row, c=col: self.click(r, c))
                         for col in range(self.cols)] for row in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                self.buttons[row][col].grid(row=row, column=col)

    def click(self, row, col):
        if self.board[row][col] == -1:
            print("Game Over! You clicked on a mine.")
            self.reveal_all()
        else:
            self.reveal_cell(row, col)

    def reveal_cell(self, row, col):
        # Implement logic to reveal the cell (update button text, change color, etc.)
        pass

    def reveal_all(self):
        # Implement logic to reveal all cells and end the game
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Démineur")
    
    # Spécifiez le nombre de lignes, de colonnes et de mines selon vos besoins
    demineur = DemineurGUI(root, rows=8, cols=8, mines=10)

    root.mainloop()









  


