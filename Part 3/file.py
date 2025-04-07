import sqlite3
import sys
import datetime

def connect_to_db():
    conn = sqlite3.connect('XYZGym.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

def print_table_header(headers, widths):
    header_row = " | ".join(f"{headers[i]:{widths[i]}}" for i in range(len(headers)))
    print(header_row)
    separator = "=" * len(header_row)
    print(separator)

def query1():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = """
    SELECT DISTINCT m.name, m.email, m.age, mp.planType
    FROM Member m
    JOIN Payment p ON m.memberId = p.memberId
    JOIN MembershipPlan mp ON p.planId = mp.planId
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Define column widths
    widths = [20, 30, 5, 15]
    headers = ["Member Name", "Email", "Age", "Plan Type"]
    
    print_table_header(headers, widths)
    
    for row in results:
        formatted_row = " | ".join([
            f"{row['name']:{widths[0]}}", 
            f"{row['email']:{widths[1]}}", 
            f"{row['age']:{widths[2]}}", 
            f"{row['planType']:{widths[3]}}"
        ])
        print(formatted_row)
    
    conn.close()

def query2():
    conn = connect_to_db()
    cursor = conn.cursor()
    
    query = """
    SELECT gf.location, COUNT(c.classId) as class_count
    FROM GymFacility gf
    LEFT JOIN Class c ON gf.gymId = c.gymId
    GROUP BY gf.gymId, gf.location
    ORDER BY class_count DESC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Define column widths
    widths = [30, 20]
    headers = ["Gym Location", "Number of Classes"]
    
    print_table_header(headers, widths)
    
    for row in results:
        formatted_row = " | ".join([
            f"{row['location']:{widths[0]}}", 
            f"{row['class_count']:{widths[1]}}"
        ])
        print(formatted_row)
    
    conn.close()

def query3(class_id=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    if class_id is None:
        class_list_query = "SELECT classId, className FROM Class"
        cursor.execute(class_list_query)
        classes = cursor.fetchall()
        
        print("Available Classes:")
        print("=" * 50)
        print("Class ID | Class Name")
        print("-" * 50)
        for cls in classes:
            print(f"{cls['classId']:8} | {cls['className']}")
        print("\nUsage: python file.py 3 <classId>")
        conn.close()
        return
    
    class_query = "SELECT className FROM Class WHERE classId = ?"
    cursor.execute(class_query, (class_id,))
    class_result = cursor.fetchone()
    
    if not class_result:
        print(f"No class found with ID {class_id}")
        conn.close()
        return
        
    class_name = class_result['className']
    
    query = """
    SELECT m.name
    FROM Member m
    JOIN Attends a ON m.memberId = a.memberId
    WHERE a.classId = ?
    """
    
    cursor.execute(query, (class_id,))
    results = cursor.fetchall()
    
    if not results:
        print(f"No members found attending class with ID {class_id} ({class_name})")
        conn.close()
        return
    
    print(f"Members attending {class_name} (ID: {class_id}):")
    print("=" * 50)
    
    for row in results:
        print(f"- {row['name']}")
    
    conn.close()

def query4(equipment_type=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    if equipment_type is None:
        types_query = "SELECT DISTINCT type FROM Equipment"
        cursor.execute(types_query)
        types = cursor.fetchall()
        
        print("Available Equipment Types:")
        print("=" * 50)
        for t in types:
            print(f"- {t['type']}")
        print("\nUsage: python file.py 4 <type>")
        conn.close()
        return
    
    query = """
    SELECT name
    FROM Equipment
    WHERE type = ?
    """
    
    cursor.execute(query, (equipment_type,))
    results = cursor.fetchall()
    
    if not results:
        print(f"No equipment found of type '{equipment_type}'")
        conn.close()
        return
    
    print(f"Equipment of type '{equipment_type}':")
    print("=" * 50)
    
    for row in results:
        print(f"- {row['name']}")
    
    conn.close()

def query5():
    conn = connect_to_db()
    cursor = conn.cursor()
    
    today = datetime.date.today().isoformat()
    
    query = """
    SELECT name, email, membershipEndDate
    FROM Member
    WHERE date(membershipEndDate) < date(?)
    """
    
    cursor.execute(query, (today,))
    results = cursor.fetchall()
    
    if not results:
        print("No members with expired memberships found")
        conn.close()
        return
    
    print("Members with Expired Memberships:")
    
    # Define column widths
    widths = [20, 30, 15]
    headers = ["Name", "Email", "End Date"]
    
    print_table_header(headers, widths)
    
    for row in results:
        formatted_row = " | ".join([
            f"{row['name']:{widths[0]}}", 
            f"{row['email']:{widths[1]}}", 
            f"{row['membershipEndDate']:{widths[2]}}"
        ])
        print(formatted_row)
    
    conn.close()

def query6(instructor_id=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    if instructor_id is None:
        # Display all instructors
        instructor_query = "SELECT instructorId, name FROM Instructor"
        cursor.execute(instructor_query)
        instructors = cursor.fetchall()
        
        print("Available Instructors:")
        print("=" * 50)
        print("Instructor ID | Instructor Name")
        print("-" * 50)
        for instructor in instructors:
            print(f"{instructor['instructorId']:13} | {instructor['name']}")
        print("\nUsage: python file.py 6 <instructorId>")
        conn.close()
        return
    
    # First check if instructor exists
    instructor_check = "SELECT name FROM Instructor WHERE instructorId = ?"
    cursor.execute(instructor_check, (instructor_id,))
    instructor_result = cursor.fetchone()
    
    if not instructor_result:
        print(f"No instructor found with ID {instructor_id}")
        conn.close()
        return
    
    query = """
    SELECT i.name as instructor_name, i.phone, c.className, c.classType, 
           c.duration, c.classCapacity
    FROM Instructor i
    JOIN Class c ON i.instructorId = c.instructorId
    WHERE i.instructorId = ?
    """
    
    cursor.execute(query, (instructor_id,))
    results = cursor.fetchall()
    
    if not results:
        print(f"No classes found for instructor {instructor_result['name']} (ID: {instructor_id})")
        conn.close()
        return
    
    print(f"Classes taught by {results[0]['instructor_name']}:")
    
    # Define column widths
    widths = [20, 15, 15, 10]
    headers = ["Class Name", "Type", "Duration (min)", "Capacity"]
    
    print_table_header(headers, widths)
    
    for row in results:
        formatted_row = " | ".join([
            f"{row['className']:{widths[0]}}", 
            f"{row['classType']:{widths[1]}}", 
            f"{row['duration']:{widths[2]}}", 
            f"{row['classCapacity']:{widths[3]}}"
        ])
        print(formatted_row)
    
    conn.close()

def query7():
    conn = connect_to_db()
    cursor = conn.cursor()
    
    today = datetime.date.today().isoformat()
    
    # Query for active members
    active_query = """
    SELECT AVG(age) as avg_age
    FROM Member
    WHERE date(membershipEndDate) >= date(?)
    """
    
    # Query for expired members
    expired_query = """
    SELECT AVG(age) as avg_age
    FROM Member
    WHERE date(membershipEndDate) < date(?)
    """
    
    cursor.execute(active_query, (today,))
    active_result = cursor.fetchone()
    active_avg_age = active_result['avg_age'] if active_result['avg_age'] is not None else 0
    
    cursor.execute(expired_query, (today,))
    expired_result = cursor.fetchone()
    expired_avg_age = expired_result['avg_age'] if expired_result['avg_age'] is not None else 0
    
    print("Average Member Age by Membership Status:")
    print("=" * 50)
    print(f"Active Memberships: {active_avg_age:.2f} years")
    print(f"Expired Memberships: {expired_avg_age:.2f} years")
    
    conn.close()

def query8():
    conn = connect_to_db()
    cursor = conn.cursor()

    #Query for top 3 instructors
    topInstructors_query = """
    SELECT instructorId, name, frequency
    FROM Instructor NATURAL JOIN (
        SELECT instructorId, COUNT(*) as frequency
        FROM Class
        GROUP BY instructorId
        ORDER BY frequency DESC
        LIMIT 3)
    """

    cursor.execute(topInstructors_query)
    topIns_result = cursor.fetchall()

    print("Top 3 Instructors:")
    print("=" * 59)

    # Define column widths
    widths = [14, 20, 10]
    headers = ["Instructor ID", "Instructor Name", "# of Classes Taught"]
    
    print_table_header(headers, widths)
    
    for row in topIns_result:
        formatted_row = " | ".join([
            f"{row['instructorId']:{widths[0]}}", 
            f"{row['name']:{widths[1]}}", 
            f"{row['frequency']:{widths[2]}}"
        ])
        print(formatted_row)

    conn.close()


def query9(class_type=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    
    if class_type is None or class_type.strip() == "":
        types_query = "SELECT DISTINCT classType FROM Class"
        cursor.execute(types_query)
        types = cursor.fetchall()
        print("Available Class Types:")
        print("=" * 50)
        for t in types:
            print(f"- {t['classType']}")
        print("\nUsage: python file.py 9 <classType>")
        conn.close()
        return
    
    members_query = """
    SELECT DISTINCT m.memberId, m.name
    FROM Member m
    JOIN Attends a ON m.memberId = a.memberId
    JOIN Class c ON a.classId = c.classId
    WHERE c.classType = ?
    """
    
    cursor.execute(members_query, (class_type,))
    results = cursor.fetchall()
    
    if not results:
        print(f"No members have attended classes of type '{class_type}'")
        conn.close()
        return
    
    print(f"Members who have attended classes of type '{class_type}':")
    print("=" * 50)
    
    for row in results:
        print(f"- {row['name']}")
    
    conn.close()

def query10():
    conn = connect_to_db()
    cursor = conn.cursor()

    #Query for recently active members
    recent_query = """
    SELECT *
    FROM Attends NATURAL JOIN MEMBER NATURAL JOIN Class
    WHERE attendanceDate >= (SELECT DATE(CURRENT_DATE, '-1 month'))
    """

    cursor.execute(recent_query)
    recent_result = cursor.fetchall()     
    
    print("Members active in last month")
    print("=" * 70)

    # Define column widths
    widths = [14, 20, 10]
    headers = ["Member Name", "Class Name", "Class Type"]
    
    print_table_header(headers, widths)
    
    for row in recent_result:
        formatted_row = " | ".join([
            f"{row['name']:{widths[0]}}", 
            f"{row['className']:{widths[1]}}", 
            f"{row['classType']:{widths[2]}}"
        ])
        print(formatted_row)

    conn.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python file.py <query_number> [additional_parameters]")
        print("\nQueries:")
        print("1: List of the members in the gym")
        print("2: Number of classes at each gym facility")
        print("3: List of members attending a specific class")
        print("4: List of equipment of a specific type")
        print("5: Members with expired memberships")
        print("6: List of classes taught by a specific instructor")
        print("7: Average age of active vs. expired members")
        print("8: Top instructors")
        print("9: Members who attend all of a certain class type")
        print("10: Recently active members")
        return
    
    query_num = sys.argv[1]
    
    try:
        if query_num == "1":
            query1()
        elif query_num == "2":
            query2()
        elif query_num == "3":
            class_id = sys.argv[2] if len(sys.argv) > 2 else None
            query3(class_id)
        elif query_num == "4":
            equipment_type = sys.argv[2] if len(sys.argv) > 2 else None
            query4(equipment_type)
        elif query_num == "5":
            query5()
        elif query_num == "6":
            instructor_id = sys.argv[2] if len(sys.argv) > 2 else None
            query6(instructor_id)
        elif query_num == "7":
            query7()
        elif query_num == "8":
            query8()
        elif query_num == "9":
            class_type = sys.argv[2] if len(sys.argv) > 2 else None
            query9(class_type)
        elif query_num == "10":
            query10()
        else:
            print(f"Invalid query number: {query_num}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
