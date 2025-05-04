# -*- coding: utf-8 -*-
"""
Created on Sat May  3 12:39:33 2025

@author: vgnod
"""

import sqlite3
from datetime import datetime
import sys

def connect_to_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}, Try again")
        main()
        

def print_table_header(headers, widths):
    header_row = " | ".join(f"{headers[i]:{widths[i]}}" for i in range(len(headers)))
    print(header_row)
    separator = "=" * len(header_row)
    print(separator)

def display_members(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Member")
    members = cursor.fetchall()
    if not members:
        print("No members found.")
        return
    headers = ["ID", "Name", "Email", "Phone", "Address", "Age", "Start Date", "End Date"]
    widths = [5, 20, 30, 15, 30, 5, 12, 12]
    print_table_header(headers, widths)
    
    for member in members:
        print(f"{member['memberId']:5} | {member['name']:20} | {member['email']:30} | "
              f"{member['phone']:15} | {member['address']:30} | {member['age']:5} | "
              f"{member['membershipStartDate']:12} | {member['membershipEndDate']:12}")

def add_member(connection):
    try:
        print("\nEnter new member details:")
        name = input("Name: ")
        email = input("Email: ")
        phone = input("Phone (optional): ")
        address = input("Address (optional): ")
        age = int(input("Age 15+: "))
        if age < 15:
            print("Age must be 15+.")
            return  
        start_date = input("Membership start date (YYYY-MM-DD): ")
        end_date = input("Membership end date (YYYY-MM-DD): ")
        
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Member (name, email, phone, address, age, membershipStartDate, membershipEndDate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, email, phone, address, age, start_date, end_date))
        connection.commit()
        print("Member added successfully!")
    except ValueError:
        print("Invalid input. Please try again.")

def update_member(connection):
    try:
        member_id = int(input("Enter member ID to update: "))
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Member WHERE memberId = ?", (member_id,))
        member = cursor.fetchone()
        
        if not member:
            print("Member not found.")
            return    
        print("\nCurrent member details:")
        print(f"1. Name: {member['name']}")
        print(f"2. Email: {member['email']}")
        print(f"3. Phone: {member['phone']}")
        print(f"4. Address: {member['address']}")
        print(f"5. Age: {member['age']}")
        print(f"6. Start Date: {member['membershipStartDate']}")
        print(f"7. End Date: {member['membershipEndDate']}")  
        field = int(input("\nEnter field number to update (1-7): "))
        new_value = input("Enter new value: ")
        
        fields = ['name', 'email', 'phone', 'address', 'age', 'membershipStartDate', 'membershipEndDate']
        cursor.execute(f"UPDATE Member SET {fields[field-1]} = ? WHERE memberId = ?", (new_value, member_id))
        connection.commit()
        print("Member updated successfully")
    except ValueError:
        print("Invalid input. Please try again.")

def delete_member(connection):
    try:
        member_id = int(input("Enter member ID to delete: "))
        cursor = connection.cursor()
        
        # Check if member exists
        cursor.execute("SELECT * FROM Member WHERE memberId = ?", (member_id,))
        if not cursor.fetchone():
            print("Member not found.")
            return
        cursor.execute("DELETE FROM Attends WHERE memberId = ?", (member_id,))
        cursor.execute("DELETE FROM Payment WHERE memberId = ?", (member_id,))
        cursor.execute("DELETE FROM Member WHERE memberId = ?", (member_id,))
        connection.commit()
        print("Member deleted successfully!")
    except ValueError:
        print("Invalid input. Please try again.")

def display_classes(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT c.*, i.name as instructor_name, g.location as gym_location,
               COUNT(a.memberId) as attendance_count
        FROM Class c
        LEFT JOIN Instructor i ON c.instructorId = i.instructorId
        LEFT JOIN GymFacility g ON c.gymId = g.gymId
        LEFT JOIN Attends a ON c.classId = a.classId
        GROUP BY c.classId
    """)
    classes = cursor.fetchall()
    if not classes:
        print("No classes found.")
        return     
    headers = ["ID", "Name", "Type", "Duration", "Capacity", "Instructor", "Gym", "Attendance"]
    widths = [5, 20, 15, 10, 10, 20, 15, 10]
    print_table_header(headers, widths)
    for class_ in classes:
        print(f"{class_['classId']:5} | {class_['className']:20} | {class_['classType']:15} | "
              f"{class_['duration']:10} | {class_['classCapacity']:10} | {class_['instructor_name']:20} | "
              f"{class_['gym_location']:15} | {class_['attendance_count']:10}")

def add_class(connection):
    try:
        print("\nEnter new class details:")
        name = input("Class name: ")
        class_type = input("Class type (Yoga/Zumba/HIIT/Weights): ")
        duration = int(input("Duration (minutes): "))
        capacity = int(input("Class capacity: "))
        instructor_id = int(input("Instructor ID: "))
        gym_id = int(input("Gym ID: "))
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymId)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, class_type, duration, capacity, instructor_id, gym_id))
        connection.commit()
        print("Class added successfully!")
    except ValueError:
        print("Invalid input. Please try again.")

def update_class(connection):
    try:

        class_id = int(input("Enter class ID to update: "))
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Class WHERE classId = ?", (class_id,))
        class_ = cursor.fetchone()
        
        if not class_:
            print("Class not found.")
            return
            
        print("\nCurrent class details:")
        print(f"1. Name: {class_['className']}")
        print(f"2. Type: {class_['classType']}")
        print(f"3. Duration: {class_['duration']}")
        print(f"4. Capacity: {class_['classCapacity']}")
        print(f"5. Instructor ID: {class_['instructorId']}")
        print(f"6. Gym ID: {class_['gymId']}")
        
        field = int(input("\nEnter field number to update (1-6): "))
        new_value = input("Enter new value: ")
        
        fields = ['className', 'classType', 'duration', 'classCapacity', 'instructorId', 'gymId']
        cursor.execute(f"UPDATE Class SET {fields[field-1]} = ? WHERE classId = ?", (new_value, class_id))
        connection.commit()
        print("Class updated successfully.")
    except ValueError:
        print("Invalid input. Please try again.")

def delete_class(connection):
    try:
        class_id = int(input("Enter class ID to delete: "))
        cursor = connection.cursor()
        # Check if class exists
        cursor.execute("SELECT * FROM Class WHERE classId = ?", (class_id,))
        if not cursor.fetchone():
            print("Class not found.")
            return
            
        # Check if class has members
        cursor.execute("SELECT COUNT(*) FROM Attends WHERE classId = ?", (class_id,))
        member_count = cursor.fetchone()[0]
        if member_count > 0:
            print(f"This class has {member_count} registered members.")
            choice = input("Do you want to move members to another class? (y/n): ")
            if choice.lower() == 'y':
                new_class_id = int(input("Enter new class ID to move members to: "))
                cursor.execute("UPDATE Attends SET classId = ? WHERE classId = ?", (new_class_id, class_id))
            else:
                print("Cannot delete class with registered members.")
                return   
        cursor.execute("DELETE FROM Class WHERE classId = ?", (class_id,))
        connection.commit()
        print("Class deleted successfully!")
    except ValueError:
        print("Invalid input. Please try again.")

def find_members_by_class(connection):
    try:
        class_id = int(input("Enter class ID to find members: "))
        cursor = connection.cursor()
        cursor.execute("""
            SELECT m.*, a.attendanceDate
            FROM Member m
            JOIN Attends a ON m.memberId = a.memberId
            WHERE a.classId = ?
        """, (class_id,))
        members = cursor.fetchall()
        
        if not members:
            print("No members found for this class.")
            return
            

        headers = ["ID", "Name", "Email", "Phone", "Address", "Age", "Attendance Date"]
        widths = [5, 20, 30, 15, 30, 5, 15]
        print_table_header(headers, widths)
        for member in members:
            print(f"{member['memberId']:5} | {member['name']:20} | {member['email']:30} | "
                  f"{member['phone']:15} | {member['address']:30} | {member['age']:5} | "
                  f"{member['attendanceDate']:15}")
    except ValueError:
        print("Invalid input. Please try again.")

def display_equipment(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT e.*, g.location as gym_location
        FROM Equipment e
        LEFT JOIN GymFacility g ON e.gymId = g.gymId
    """)
    equipment = cursor.fetchall()
    if not equipment:
        print("No equipment found.")
        return
        
    headers = ["ID", "Name", "Type", "Quantity", "Gym Location"]
    widths = [5, 20, 15, 10, 20]
    print_table_header(headers, widths)
    for item in equipment:
        print(f"{item['equipmentId']:5} | {item['name']:20} | {item['type']:15} | "
              f"{item['quantity']:10} | {item['gym_location']:20}")

def add_equipment(connection):
    try:
        print("\nEnter new equipment details:")
        name = input("Equipment name: ")
        type_ = input("Type (Cardio/Strength/Flexibility/Recovery): ")
        quantity = int(input("Quantity: "))
        gym_id = int(input("Gym ID: "))
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Equipment (name, type, quantity, gymId)
            VALUES (?, ?, ?, ?)
        """, (name, type_, quantity, gym_id))
        connection.commit()
        print("Equipment added successfully!!")
    except ValueError:
        print("Invalid input. Please try again.")

def update_equipment(connection):
    try:
        equipment_id = int(input("Enter equipment ID to update: "))
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Equipment WHERE equipmentId = ?", (equipment_id,))
        equipment = cursor.fetchone()
        
        if not equipment:
            print("Equipment not found.")
            return
            
        print("\nCurrent equipment details:")
        print(f"1. Name: {equipment['name']}")
        print(f"2. Type: {equipment['type']}")
        print(f"3. Quantity: {equipment['quantity']}")
        print(f"4. Gym ID: {equipment['gymId']}")
        
        field = int(input("\nEnter field number to update (1-4): "))
        new_value = input("Enter new value: ")
        fields = ['name', 'type', 'quantity', 'gymId']
        cursor.execute(f"UPDATE Equipment SET {fields[field-1]} = ? WHERE equipmentId = ?", (new_value, equipment_id))
        connection.commit()
        print("Equipment updated successfully!")
    except ValueError:
        print("Invalid input. Please try again.")

def delete_equipment(connection):
    try:
        equipment_id = int(input("Enter equipment ID to delete: "))
        cursor = connection.cursor()

        # Check if equipment exists
        cursor.execute("SELECT * FROM Equipment WHERE equipmentId = ?", (equipment_id,))
        if not cursor.fetchone():
            print("Equipment not found.")
            return   
        cursor.execute("DELETE FROM Equipment WHERE equipmentId = ?", (equipment_id,))
        connection.commit()
        print("Equipment deleted successfully!")
    except ValueError:
        print("Invalid input. Please try again.")

def members_menu(connection):
    while True:
        print("\nMembers Menu")
        print("1. Display all members")
        print("2. Add new member")
        print("3. Update member information")
        print("4. Delete member")
        print("5. Back to main menu")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            display_members(connection)
        elif choice == "2":
            add_member(connection)
        elif choice == "3":
            update_member(connection)
        elif choice == "4":
            delete_member(connection)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def classes_menu(connection):
    while True:
        print("\nClasses Menu")
        print("1. Display all classes")
        print("2. Add new class")
        print("3. Update class information")
        print("4. Delete class")
        print("5. Find members by class")
        print("6. Back to main menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            display_classes(connection)
        elif choice == "2":
            add_class(connection)
        elif choice == "3":
            update_class(connection)
        elif choice == "4":
            delete_class(connection)
        elif choice == "5":
            find_members_by_class(connection)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

def equipment_menu(connection):
    while True:

        print("\nEquipment Menu")
        print("1. Display all equipment")
        print("2. Add new equipment")
        print("3. Update equipment details")
        print("4. Delete equipment")
        print("5. Back to main menu")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            display_equipment(connection)
        elif choice == "2":
            add_equipment(connection)
        elif choice == "3":
            update_equipment(connection)
        elif choice == "4":
            delete_equipment(connection)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def menu(connection):
    while True:

        print("\nMain Menu")
        print("1. Members Menu")
        print("2. Classes Menu")
        print("3. Equipment Menu")
        print("4. Logout and exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            members_menu(connection)
        elif choice == "2":
            classes_menu(connection)
        elif choice == "3":
            equipment_menu(connection)
        elif choice == "4":
            print("Logging off, Thank you!")
            connection.close()
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

def main():
    db_name = input("Enter name of database:: ")
    connection = connect_to_db(db_name)
    menu(connection)

if __name__ == "__main__":
    main()