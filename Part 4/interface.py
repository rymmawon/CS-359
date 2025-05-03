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

def main_menu():
    print("\nMain Menu")
    print("\n1. Members Menu")
    print("\n2. Classes Menu")
    print("\n3. Equipment Menu")
    print("\n4. Logout and exit")
    
def members_menu():
    print("\nMembers Menu")
    print("\n1. Display all members")
    print("\n2. Add new member")
    print("\n3. Update member information")
    print("\n4. Delete member")
    print("\n5. Back to main menu")
    choice = input("Enter your choice: ")

def display_all_members():
    print("Member List")

def add_member():
    print("Input member Info")
    name = input("Member's Full name: ")
    age = input("Member's Age: ")
    gender = input("Members gender: ")

def update_member():
    print("Search for desired member")
    
def delete_member():
    print("Deleting desired member")
    #have to delete them from all tables
    
def classes_menu():
    print("\nClasses Menu")
    print("\n1. Display all classes")
    print("\n2. Add new class")
    print("\n3. Update class information")
    print("\n4. Delete class")
    print("\n5. Find members by class")
    print("\n6. Back to main menu")
    choice = input("Enter your choice: ")

def display_all_classes():
    print("Class List")

def add_class():
    print("Input class Info")
    name = input("Class name: ")
    c_type = input("Class type: ")
    duration = input("Class duration: ")
    limit = input("Class enrollment limit: ")

def update_class():
    print("Search for desired class")
    
def delete_class():
    print("Deleting desired class")
    #have to delete them from all tables
    
def equipment_menu():
    print("\nEquipment Menu")
    print("\n1. Display all equipment")
    print("\n2. Insert new equipment")
    print("\n3. Update equipment details")
    print("\n4. Delete equipment")
    print("\n5. Back to main menu")
    choice = input("Enter your choice: ")

def display_all_equipment():
    print("Equipment Inventory")

def insert_equipment():
    print("Input equipment Info")
    name = input("Equipment name: ")
    e_type = input("Equipment Type: ")
    quantity = input("Equipment quantity: ")

def update_equipment():
    print("Search for desired member")
    
def delete_equipment():
    print("Deleting desired member")
    #have to delete them from all tables
    
def logout():
    print("Logging off, Thank you!")
    exit()
    
def menu():
    
    main_menu()
    choice = input("Enter your choice: ")
    
    if choice == '1':
        members_menu()
    elif choice == '2':
        classes_menu()
    elif choice == '3':
        equipment_menu()
    elif choice == '4':
        logout()
    else:
        print("\nInvalid choice. Please try again.")
            
if __name__ == "__main__":
    menu()