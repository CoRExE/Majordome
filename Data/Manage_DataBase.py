#  Copyright (c) 2024.
#  Ceci est une propriété de CoRExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import os
import sqlite3 as sql
from os.path import exists


class ManageDB:
    def __init__(self, home_schema: str):
        """
        Initialise un tableau de données en lisant les fichiers situé dans le Dossier Home_Schema
        Deux Variables Connection et Cursor visant à accueillir les objets de même nom du module Sqlite3
        """
        print(os.getcwd())
        if not exists(home_schema):
            os.mkdir(home_schema)
        self.home_schema = home_schema
        self.schemas = [schema[:-3] for schema in os.listdir(home_schema) if schema.endswith(".db")]
        self.tables = {}
        self.current_schema = None
        self.connection = None
        self.cursor = None
        if self.schemas:
            for schema in self.schemas:
                self.tables[schema] = []
                self.connexion(schema)
                self.safe_close()

    def create_schema(self, schema: str):
        """
        Prends en paramètre un nom de schema et vérifie s'il existe
        Enregistre ça création dans la liste des schemas, et en cle dans
        le dictionnaire tables et lui attribut une liste en valeur
        :param schema:
        :return:
        """
        assert schema not in self.schemas, "Le Schema existe déjà"
        self.connection = sql.connect(f"./{self.home_schema}/{schema}.db")
        self.schemas.append(schema)
        self.tables[schema] = []

    def delete_schema(self, schema: str):
        """
        Prends en paramètre un nom de schema et vérifie s'il existe
        Supprime la table ainsi que le schema
        :param schema:
        :return:
        """
        assert schema in self.schemas, "Le Schema n'existe pas"
        self.connection = sql.connect(f"./{self.home_schema}/{schema}.db")
        self.schemas.remove(schema)
        self.tables.pop(schema)

    # Manage Methods
    def connexion(self, schema: str) -> bool:
        """
        Appel la méthode close_all pour établir une connexion
        sécurisé et ne pas perdre les données précédemment saisies

        Enfin, vérifie si la table demandée existe, et établie
        la connexion ainsi qu'un curseur sur celle-ci

        Retourne le Bon ou mauvais déroulement de la fonction avec un booléen
        :param schema:
        :return bool:
        """
        self.safe_close()
        if schema in self.schemas:
            self.connection = sql.connect(f"./{self.home_schema}/{schema}.db")
            self.cursor = self.connection.cursor()
            for table in self.cursor.execute("select name from sqlite_master where type='table';").fetchall():
                if table[0] not in self.tables[schema]:
                    self.tables[schema].append(table[0])
            self.current_schema = schema
            print(f"Connexion Établie avec la Base de donnée {schema}")
            return True
        else:
            print("La base de données n'existe pas")
            return False

    def check_connexion(self) -> bool:
        """
        Vérifie si une connexion est actuellement ouverte et retourne directement le résultat du test
        :return bool:
        """
        return self.cursor is not None and self.connection is not None and self.current_schema is not None

    def save(self) -> bool:
        """
        Vérifie la connexion
        Sauvegarde les modifications réalisées dans la base de données actuellement connectée
        :return bool:
        """
        if self.check_connexion():
            self.connection.commit()
            print("Modification(s) Sauvegardée(s)")
            return True
        else:
            print("Nothing to Save")
            return False

    def safe_close(self):
        """
        Réaliser une confirmation de management
        Ferme la connexion avec la base de données de manière sécurisée
        Sauvegarde les modifications effectuées
        :return:
        """
        if self.save():
            self.cursor.close()
            self.connection.close()
            print("Connexion End")
            self.current_schema, self.cursor, self.connection = None, None, None
        else:
            print("Nothing to close")
            return False

    def force_close(self):
        """
        Vérifie tout de même si une connexion est ouverte
        pour éviter toute erreur et ferme la connexion sans
        sauvegarder les changements
        :return:
        """
        if self.check_connexion():
            self.cursor.close()
            self.connection.close()
            self.current_schema, self.cursor, self.connection = None, None, None
        else:
            print("Nothing to Close")
            return False

    def show_tables(self, schema) -> list:
        """
        Retourne une liste de tables d'un schéma particulier
        fourni en paramètre
        :param schema:
        :return list:
        """
        return self.tables[schema]

    # Manipulation Methods
    def create_table(self, args: str) -> bool:
        """
        Réalise une vérification sur la commande sur les deux premiers mots
        Et execute la commande en vérifiant la connexion sans vérification supplémentaire
        :param args:
        :return bool:
        """
        assert args[:6] == "CREATE" and args[7:12] == "TABLE", "Command must be CREATE TABLE"
        if self.check_connexion() and args.split(" ")[2] not in self.tables[self.current_schema]:
            self.cursor.execute(args)
            self.tables[self.current_schema].append((args.split(" ")[2]))
            return True
        else:
            print("Aucune connexion établie ou La table existe deja")
            return False

    def delete_table(self, args):
        """
        Réalise une vérification de commande sur le premier mot
        Puis vérifie si la table existe
        Et execute la suppression de la table
        :param args:
        :return:
        """
        assert args[0:4] == "DROP" and args[5:10] == "TABLE", "Command must be DROP TABLE"
        if args.split(" ")[2] in self.tables[self.current_schema] and self.check_connexion():
            self.cursor.execute(args)
            self.tables[self.current_schema].remove(args.split(" ")[2])
        else:
            print("La table n'existe pas ou aucune connexion établie")
            return False

    def insertion(self, args: str):
        """
        Réalise une verification de commande sur les premiers mots
        Et execute l'ajout de données sans vérification supplémentaire
        :param args:
        :return:
        """
        assert args[0:6] == "INSERT" and args[7:11] == "INTO", "Command must be INSERT INTO"
        if self.check_connexion() and args.split(" ")[2] in self.tables[self.current_schema]:
            self.cursor.execute(args)
        else:
            print("La table n'existe pas ou aucune connexion établie")
            return False

    def delete_data(self, args: str):
        """
        Réalise une verification de commande sur les premiers mots
        Et execute la suppression de données sans vérification supplémentaire
        :param args:
        :return:
        """
        assert args[0:6] == "DELETE" and args[7:11] == "FROM", "Command must be DELETE FROM"
        if self.check_connexion() and args.split(" ")[2] in self.tables[self.current_schema]:
            self.cursor.execute(args)
        else:
            print("La table n'existe pas ou aucune connexion établie")
            return False

    def selection(self, args: str) -> list | bool:
        """
        Réalise une vérification de commande sur le premier mot
        Et Affiche tous les résultats de la sélection
        :param args:
        :return data <list[tuple]>:
        """
        assert args[0:6] == "SELECT", "Command must be SELECT"
        if self.check_connexion() and args.split("FROM")[1][1:] in self.tables[self.current_schema]:
            data = self.cursor.execute(args).fetchall()
            return data
        else:
            print("La table n'existe pas ou aucune connexion établie")
            return False

    def simple_create_table(self, table: str, columns: list[tuple]):
        """
        Créer une table simplement en donnant son nom et ses colonnes
        :param table:
        :param columns:
        :return:
        """
        args = "CREATE TABLE " + table + " ("
        for column in columns:
            args += column[0] + " " + column[1] + ", "
        args = args[:-2] + ");"
        self.create_table(args)

    def simple_create_tables(self, tables: list[str, list[tuple]]):
        """
        Créer une table simplement en donnant son nom et ses colonnes
        :param tables:
        :return:
        """
        for table in tables:
            self.simple_create_table(table[0], table[1])

    def simple_delete_table(self, table: str):
        """
        Supprime une table simplement en donnant son nom
        :param table:
        :return:
        """
        args = "DROP TABLE " + table + ";"
        self.delete_table(args)

    def simple_insertion(self, table: str, columns: list, values: list[tuple]):
        """
        Ajoute des données à une table simplement en donnant son nom, ses colonnes et ses données
        :param table:
        :param columns:
        :param values:
        :return:
        """
        args = "INSERT INTO " + table + " ("
        for column in columns:
            args += (column + ", ")
        args = args[:-2] + ") VALUES "
        for value in values:
            args += "("
            for val in value:
                args += (str(val) + ", ")
            args = args[:-2] + "), "
        args = args[:-2] + ";"
        self.insertion(args)

    def simple_selection(self, table: str, columns: list | str = "*", conditions: list[str] = None):
        """
        Affiche les données d'une table simplement en donnant son nom et ses colonnes
        :param table:
        :param columns:
        :param conditions:
        :return:
        """
        args = "SELECT "
        if type(columns) is list:
            for column in columns:
                args += (column + ", ")
            args = args[:-2]
        else:
            args += columns
        args += " FROM " + table
        if conditions is not None:
            for condition in conditions:
                args += " " + condition
        return self.selection(args)
