import pymysql
import sys
from datetime import datetime, date
con = pymysql.connect(host='localhost', user='YOUR_MYSQL_USERNAME', password='YOUR_MYSQL_PASSWORD', charset='utf8')
c = con.cursor()
c.execute("USE USE YOUR_DATABASE_NAME")

def get_age(dob_input):
    if isinstance(dob_input, str):
        dob = datetime.strptime(dob_input, '%Y-%m-%d').date()
    else:
        dob = dob_input
    
    today = date.today()
    age = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    return age

# 1. EXACT AGE LIMITS CHECK
def check_age_limit(dob_input, category):
    age = get_age(dob_input)
    
    limits = {'U8':(3,8), 'U10':(8,10), 'U12':(10,12), 'U14':(12,14),
              'U16':(14,16), 'U18':(16,18), 'U20':(18,20), 'Senior':(20,100)}
    
    if category not in limits:
        print("ERROR: Invalid category!")
        return False
    min_age, max_age = limits[category]
    if not (min_age <= age <= max_age):
        print(f"ERROR: Age {age} not in range {min_age}-{max_age} for {category}!")
        return False
    print(f"OK: Age {age} valid for {category}")
    return True

# 2. PLAYER ELIGIBILITY CHECK (PRE-CONDITION)
def player_eligible(pid):
    c.execute("SELECT membership_status, dob, age_category FROM players WHERE player_id=%s", (pid,))
    result = c.fetchone()
    
    if not result:
        print(f"ERROR: Player {pid} not found!")
        return False
    
    status, dob, category = result
    if status != 'Active':
        print(f"ERROR: Player {pid} is {status}!")
        return False
    
    age = get_age(dob)
    if age < 8:
        print(f"ERROR: Player {pid} too young ({age} years)!")
        return False
    
    print(f"OK: Player {pid} eligible!")
    return True

# 3. QUORUM CHECK 
def check_quorum(min_needed=2):
    c.execute("SELECT COUNT(*) FROM officials WHERE is_active=1")
    active = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM officials WHERE is_active=0")
    inactive = c.fetchone()[0]
    print(f"Number of inactive officials are {inactive}")
    if active < min_needed:
        print(f"ERROR: Need {min_needed} officials. Only {active} active!")
        return False
    print(f"OK: Quorum met ({active} active officials)")
    return True

#3.0 Active and Inactive Officials
def active_inactive():
    c.execute("SELECT COUNT(*) FROM officials WHERE is_active=1")
    active = c.fetchone()[0]
    print(f"Number of active officials are {active}")
    c.execute("SELECT COUNT(*) FROM officials WHERE is_active=0")
    inactive = c.fetchone()[0]
    print(f"Number of inactive officials are {inactive}")
    
# 4. ILLEGAL ELECTION CHECK
def election_legal(oid):
    c.execute("SELECT term_end, is_active FROM officials WHERE official_id=%s", (oid))
    result = c.fetchone()
    if result and result[1] == 1 and result[0] > date.today():
        print(f"ERROR: Official {oid} term active until {result[0]}!")
        return False
    return True
    
# LOGIN
def login():
    print("\n=== LOGIN ===")
    print("1- LOGIN  2- NEW USER  0- EXIT")
    ch = input("Choice: ")
    
    if ch == '1':
        user = input("Username: ")
        c.execute("SELECT Passwd FROM login WHERE Uname=%s", (user))
        result = c.fetchone()
        if result:
            pwd = input("Password: ")
            if result[0] == pwd:
                print("LOGIN OK!")
                main_menu()
            else:
                print("WRONG PASSWORD!")
                login()
        else:
            print("USER NOT FOUND!")
            login()
    elif ch == '2':
        user = input("New Username: ")
        c.execute("SELECT * FROM login WHERE Uname=%s", (user))
        if not c.fetchone():
            pwd = input("New Password: ")
            c.execute("INSERT INTO login VALUES (%s,%s)", (user, pwd))
            con.commit()
            print("NEW USER CREATED!")
        else:
            print("USERNAME EXISTS!")
        login()
        
# MAIN MENU
def main_menu():
    while True:
        print("\n=== CHESS FEDERATION SYSTEM ===")
        print("Press 1 for- ADD OR VEIW PLAYER")
        print("Press 2 for- Veiw OR Log Tournaments")
        print("Press 3 for- ELECT OR VEIW OFFICIAL")
        print("Press 4 for- UPDATE RATING OR AGE")
        print("Press 5 for- SHOW OR LOG DISPUTES")
        print("Press 0 for- LOGOUT")
        ch = input("Choice(0-5): ")

        
        if ch == '1':
            print("\n=== Add or Veiw Players ===")
            print("Press 1 to- Add Players")
            print("Press 2 to- Veiw Current Players")
            ch1=int(input("Choice(1-2): "))
            if ch1 == 1:
                add_player()
            elif ch1 == 2:
                print("\n--- Current Players ---")
                c.execute("SELECT * FROM players")
                rec = c.fetchall()
                for row in rec:
                    print(row)
        elif ch == '2':
            print("\n=== Veiw or Log Tournaments ===")
            print("Press 1 to- Log Tournaments")
            print("Press 2 for- Veiw Tournaments AND Finances")
            ch3=int(input("Choice(1-2): "))
            if ch3 == 1:
                tournament_entry()
            elif ch3 == 2:
                print("\n--- Current tournaments ---")
                c.execute("SELECT * FROM tournaments")
                rec = c.fetchall()
                for row in rec:
                    print(row)
                print("\n--- Current Finances ---")
                c.execute("SELECT * FROM finances")
                re = c.fetchall()
                for row in re:
                    print(row)
        elif ch == '3':
            print("\n=== Elect or Veiw Officials ===")
            print("Press 1 to- Elect Officials")
            print("Press 2 for- Veiw Current Officials")
            ch2=int(input("Choice(1-2): "))
            if ch2 == 1:
                elect_official()
            elif ch2 == 2:
                print("\n--- Current Officials ---")
                active_inactive()
                c.execute("SELECT * FROM Officials")
                rec = c.fetchall()
                for row in rec:
                    print(row)
            
        elif ch == '4':
            print("\n=== Rating or Age Updation ===")
            print("Press 1 for- Update Rating")
            print("Press 2 for- Update Age")
            ch=int(input("Choice(1-2): "))
            if ch == 1:
                update_rating()
            elif ch == 2:
                update_age()
            else:
                print("Invalid choice!")
        elif ch == '5':
            print("\n=== Veiw or Log Disputes ===")
            print("Press 1 to- Log Disputes")
            print("Press 2 to- Veiw Disputes")
            h=int(input("Choice(1-2): "))
            if h == 1:
                pid = int(input("Player ID: "))
                oid = int(input("Official ID: "))
                reason = input("Reason of the Dispute: ")
                log_court_challenge(pid, oid, reason)
            if h == 2:
                show_disputes()
            else:
                print("Invalid choice!")
        elif ch == '0':
            print("LOGGING OUT!")
            break
        else:
            print("WRONG CHOICE!")
            login()

# 1. ADD PLAYER (AGE LIMITS)
def add_player():
    pid = int(input("Player ID: "))
    c.execute("SELECT player_id FROM players WHERE player_id=%s", (pid,))
    if c.fetchone():
        print("ID ALREADY EXISTS!")
        print("\n--- Current Players ---")
        c.execute("SELECT * FROM players")
        rec = c.fetchall()
        for row in rec:
            print(row)
        return
    
    name = input("Name: ")
    dob = input("DOB (YYYY-MM-DD): ")
    
    # AGE LIMIT CHECK
    cat = input("Category (U8/U10/U12/U14/U16/U18/U20/Senior): ")
    if not check_age_limit(dob, cat):
        return
    
    phone = input("Phone (10 digits): ")
    if len(phone) != 10:
        print("WRONG PHONE NUMBER!")
        return
    
    email = input("Email: ")
    rating = input("Rating (1000): ")
    rating = int(rating) if rating.isdigit() else 1000

    c.execute("INSERT INTO players VALUES (%s,%s,%s,%s,%s,%s,%s,'Active',CURDATE())", 
                  (pid, name, dob, cat, rating, int(phone), email))
    con.commit()
    print("PLAYER ADDED!")
        
    
# 2. TOURNAMENT ENTRY (ELIGIBILITY+FINANCE)
def tournament_entry():
    tid = int(input("Tournament ID: "))
    pid = int(input("Player ID: "))
    typ = input("Which type of Tournament('Swiss','Round Robin'): ")

    # PRE-CONDITION 1: PLAYER ELIGIBLE?
    if not player_eligible(pid):
        log_court_challenge(pid, None, "Ineligible player")
        return
    
    # PRE-CONDITION 2: QUORUM?
    if not check_quorum(2):
        return

    entryfee = float(input("Entry Fee: "))
    admin_fee = round(entryfee * 0.2, 2) 
    prizepool = round(entryfee - admin_fee, 2)
    
    print(f"Entry Fee: {entryfee}, Admin Fee: {admin_fee}, Prize Pool: {prizepool}")
    
    c.execute("""INSERT INTO tournaments (tournament_id, name, start_date, end_date, format, entry_fee, total_prize) VALUES (%s, (SELECT name FROM players WHERE player_id = %s),
                         CURDATE(), DATE_ADD(CURDATE(), INTERVAL 20 DAY), %s, %s, %s)""", 
              (tid, pid, typ, entryfee, prizepool))
    
    c.execute("""INSERT INTO finances (tournament_id, player_id, trans_date, admin_fee, price, entryfee) VALUES (%s, %s, CURDATE(), %s, %s, %s)""",
              (tid, pid, admin_fee, prizepool, entryfee))
    
    con.commit() 
    print("TOURNAMENT ENTRY OK!")

# 3. ELECT OFFICIAL (4-YEAR TERM)
def elect_official():
    # QUORUM CHECK
    if not check_quorum(3):
        return
    
    oid = int(input("Official ID: "))
    
    # ILLEGAL ELECTION CHECK
    if not election_legal(oid):
        log_court_challenge(None, oid, "Illegal election")
        return
    
    name = input("Name: ")
    role = input("Role('President','Secretary','Treasurer','Arbiter','Committee'): ")
    phone = input("Phone: ")
    email = input("Email: ")
    # EXACT 4-YEAR TERM
    start_date = date.today()
    end_date = date(start_date.year + 4, start_date.month, start_date.day)
    c.execute("INSERT INTO officials VALUES (%s,%s,%s,%s,%s,%s,%s,1)",(oid, name, role, phone, email, start_date, end_date))
    con.commit()
    print(f"ELECTED until {end_date}!")
    
# 4. UPDATE RATING OR AGE (NEEDS ELIGIBILITY)
def update_rating():
    pid = int(input("Player ID: "))
    if player_eligible(pid):
        new_rating = int(input("New Rating: "))
        c.execute("UPDATE players SET fide_rating=%s WHERE player_id=%s", (new_rating, pid))
        con.commit()
        print("RATING UPDATED!")

def update_age():
    pid = int(input("Player ID: "))
    age = input("Updated Age(In date format please): ")
    category = input("Category (U8/U10/U12/U14/U16/U18/U20/Senior): ")
    c.execute("UPDATE players SET dob = %s, age_category = %s WHERE player_id = %s", (age, category , pid))        
    con.commit()
    print("Age updated!")
    
# 5. SHOW COURT CHALLENGES AND COURT CHALLENGE LOG
def show_disputes():
    from datetime import date
    c.execute("SELECT * FROM disputes ORDER BY created_date DESC LIMIT 5")
    print("\nCOURT CHALLENGES:")
    for row in c.fetchall():
        formatted_row = []
        for item in row:
            if isinstance(item, date):
                formatted_row.append(item.strftime('%Y-%m-%d'))
            else:
                formatted_row.append(str(item))
        print(formatted_row)


def log_court_challenge(pid, oid, reason):
    c.execute("""INSERT INTO disputes (player_id, official_id, type, description, resolution_date, created_date) VALUES (%s, %s, 'Eligibility', %s, DATE_ADD(CURDATE(), INTERVAL 15 DAY),
              CURDATE())""", (pid, oid, reason))
    con.commit()
    print("COURT CHALLENGE LOGGED!")


# START PROGRAM
print("CHESS FEDERATION SYSTEM STARTED!")
login()
