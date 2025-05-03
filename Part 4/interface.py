# -*- coding: utf-8 -*-
"""
Created on Sat May  3 12:39:33 2025

@author: vgnod
"""

import sqlite3

def connect_to_db():
    conn = sqlite3.connect('XYZGym.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def print_table_header(headers, widths):
    header_row = " | ".join(f"{headers[i]:{widths[i]}}" for i in range(len(headers)))
    print(header_row)
    separator = "=" * len(header_row)
    print(separator)

def main_menu(connection):
    print("\nMain Menu")
    print("\n1. Members Menu")
    print("\n2. Classes Menu")
    print("\n3. Equipment Menu")
    print("\n4. Logout and exit")
    
def members_menu(connection):
    print("\nMembers Menu")
    print("\n1. Display all members")
    print("\n2. Add new member")
    print("\n3. Update member information")
    print("\n4. Delete member")
    print("\n5. Back to main menu")
    choice = input("Enter your choice: ")
    
def classes_menu(connection):
    print("\nClasses Menu")
    print("\n1. Display all classes")
    print("\n2. Add new class")
    print("\n3. Update class information")
    print("\n4. Delete class")
    print("\n5. Find members by class")
    print("\n6. Back to main menu")
    choice = input("Enter your choice: ")
    
def equipment_menu(connection):
    print("\nEquipment Menu")
    print("\n1. Display all equipment")
    print("\n2. Insert new equipment")
    print("\n3. Update equipment details")
    print("\n4. Delete equipment")
    print("\n5. Back to main menu")
    choice = input("Enter your choice: ")
    
def display(table):
    print(table + " List")

def add(table):
    print("Input " + table + " Info")
    
    name = input("name: ")
    c_type = input("type: ")
    duration = input("Class duration: ")
    limit = input("Class enrollment limit: ")

def update(table):
    print("Search for desired " + table)
    
def delete(table):
    print("Deleting desired " + table)
    #have to delete them from all tables
    
def logout():
    print("Logging off, Thank you!")
    exit()
    
def menu(connection):
    
    main_menu()
    choice = input("Enter your choice: ")
    
    if choice == '1':
        members_menu(connection)
    elif choice == '2':
        classes_menu(connection)
    elif choice == '3':
        equipment_menu(connection)
    elif choice == '4':
        logout()
    else:
        print("\nInvalid choice. Please try again.")

def main():
    database = input("Enter name of database:")
    
    if database == "XYZGym":
        menu(connect_to_db())
            
if __name__ == "__main__":
    main()