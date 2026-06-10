# RON THIS (in venv or conda):
# python3 -m venv .venv
# .venv/bin/activate
# pip install mysql-connector-python
# brew install mysql 

# DONT SET A PASSWORD (if u do just edit the code)

# brew services start mysql
# .venv/bin/python project.py  

# if it doesnt run cd to the right directory
# if it doesnt work make sure the mysql server is running

import mysql.connector
import argparse
import csv
import os



def connect_db():
    mydb =mysql.connector.connect(user='test', password='password', database='cs122a')
    return mydb

    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password=""
    # )
    # return mydb


def import_data(cursor, conn, folder_name):
    try:
        # cursor.execute("DROP DATABASE IF EXISTS cs122a")
        # cursor.execute("CREATE DATABASE cs122a")
        # cursor.execute("USE cs122a")

        try:
            cursor.execute("CREATE DATABASE cs122a")
        except:
            pass
        cursor.execute("USE cs122a")

        create_tables(cursor)
        conn.commit()

        table_order = [
            ('User', 'User'),
            ('Organizer', 'Organizer'),
            ('Participant', 'Participant'),
            ('Administrator', 'Administrator'),
            ('Event', 'Event'),
            ('Venue', 'Venue'),
            ('OnCampus', 'OnCampus'),
            ('OffCampus', 'OffCampus'),
            ('Slot', 'Slot'),
            ('Hosting', 'Hosting'),
            ('Approval', 'Approval')
        ]

        for csv_file, table_name in table_order:
            file_path = os.path.join(folder_name, f"{csv_file}.csv")
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if table_name == 'User':
                            parsed_row = [int(row[0]), row[1], row[2], row[3]]
                            cursor.execute("INSERT INTO User VALUES (%s, %s, %s, %s)", parsed_row)
                        elif table_name == 'Organizer':
                            parsed_row = [int(row[0]), row[1], int(row[2])]
                            cursor.execute("INSERT INTO Organizer VALUES (%s, %s, %s)", parsed_row)
                        elif table_name == 'Participant':
                            parsed_row = [int(row[0]), row[1] if row[1] != 'NULL' else None]
                            cursor.execute("INSERT INTO Participant VALUES (%s, %s)", parsed_row)
                        elif table_name == 'Administrator':
                            parsed_row = [int(row[0]), row[1], row[2]]
                            cursor.execute("INSERT INTO Administrator VALUES (%s, %s, %s)", parsed_row)
                        elif table_name == 'Event':
                            parsed_row = [int(row[0]), int(row[1]), row[2], row[3], row[4]]
                            cursor.execute("INSERT INTO Event VALUES (%s, %s, %s, %s, %s)", parsed_row)
                        elif table_name == 'Venue':
                            parsed_row = [int(row[0]), row[1], row[2], row[3], row[4]]
                            cursor.execute("INSERT INTO Venue VALUES (%s, %s, %s, %s, %s)", parsed_row)
                        elif table_name == 'OnCampus':
                            parsed_row = [int(row[0]), row[1]]
                            cursor.execute("INSERT INTO OnCampus VALUES (%s, %s)", parsed_row)
                        elif table_name == 'OffCampus':
                            parsed_row = [int(row[0]), int(row[1])]
                            cursor.execute("INSERT INTO OffCampus VALUES (%s, %s)", parsed_row)
                        elif table_name == 'Slot':
                            is_reserved = row[2] == '1'
                            uid = int(row[3]) if row[3] != 'NULL' else None
                            parsed_row = [int(row[0]), int(row[1]), is_reserved, uid]
                            cursor.execute("INSERT INTO Slot VALUES (%s, %s, %s, %s)", parsed_row)
                        elif table_name == 'Hosting':
                            is_primary = row[2] == '1'
                            parsed_row = [int(row[0]), int(row[1]), is_primary]
                            cursor.execute("INSERT INTO Hosting VALUES (%s, %s, %s)", parsed_row)
                        elif table_name == 'Approval':
                            parsed_row = [int(row[0]), int(row[1]), row[2], row[3]]
                            cursor.execute("INSERT INTO Approval VALUES (%s, %s, %s, %s)", parsed_row)

        conn.commit()
        print("Success")
    except Exception as e:
        print("Fail")

def insert_admin(cursor, conn, uid, email, username, joined, firstname, lastname):
    try:
        cursor.execute("SELECT COUNT(*) FROM User WHERE uid = %s", (uid,))
        if cursor.fetchone()[0] > 0:
            print("Fail")
            return

        cursor.execute("INSERT INTO User VALUES (%s, %s, %s, %s)", (uid, email, username, joined))
        cursor.execute("INSERT INTO Administrator VALUES (%s, %s, %s)", (uid, firstname, lastname))

        conn.commit()
        print("Success")
    except Exception as e:
        print("Fail")

def add_venue(cursor, conn, eid, vid, is_primary):
    try:
        if is_primary:
            cursor.execute("SELECT COUNT(*) FROM Hosting WHERE eid = %s AND is_primary = TRUE", (eid,))
            if cursor.fetchone()[0] > 0:
                print("Fail")
                return

        cursor.execute("INSERT INTO Hosting VALUES (%s, %s, %s)", (eid, vid, is_primary))
        conn.commit()
        print("Success")
    except Exception as e:
        print("Fail")

def create_tables(cursor):
    # # cursor.execute("DROP DATABASE IF EXISTS cs122a")
    # cursor.execute("CREATE DATABASE cs122a")
    # cursor.execute("USE cs122a")
    try:
        cursor.execute("CREATE DATABASE cs122a")
    except:
        pass
    cursor.execute("USE cs122a")

    cursor.execute("""
    CREATE TABLE User (
        uid INT,
        email TEXT NOT NULL,
        username TEXT NOT NULL,
        joined DATE NOT NULL,
        PRIMARY KEY (uid)
    )
    """)

    cursor.execute("""
    CREATE TABLE Organizer (
        uid INT,
        department TEXT NOT NULL,
        experience INT NOT NULL,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE Participant (
        uid INT,
        type TEXT,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE Administrator (
        uid INT,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE Event (
        eid INT,
        creator_uid INT NOT NULL,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        datetime DATETIME NOT NULL,
        PRIMARY KEY (eid),
        FOREIGN KEY (creator_uid) REFERENCES Organizer(uid) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE Slot (
        eid INT,
        snum INT NOT NULL,
        is_reserved BOOLEAN NOT NULL,
        uid INT,
        PRIMARY KEY (eid, snum),
        FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
        FOREIGN KEY (uid) REFERENCES Participant(uid) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE Venue (
        vid INT,
        street TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        zip TEXT NOT NULL,
        PRIMARY KEY (vid)
    )
    """)

    cursor.execute("""
    CREATE TABLE OnCampus (
        vid INT,
        code TEXT NOT NULL,
        PRIMARY KEY (vid),
        FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE OffCampus (
        vid INT,
        distance INT NOT NULL,
        PRIMARY KEY (vid),
        FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE Hosting (
        eid INT NOT NULL,
        vid INT NOT NULL,
        is_primary BOOLEAN NOT NULL,
        PRIMARY KEY (eid, vid),
        FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
        FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE Approval (
        uid INT NOT NULL,
        vid INT NOT NULL,
        valid_from DATE NOT NULL,
        valid_until DATE NOT NULL,
        PRIMARY KEY (uid, vid),
        FOREIGN KEY (uid) REFERENCES Administrator(uid) ON DELETE CASCADE,
        FOREIGN KEY (vid) REFERENCES OffCampus(vid) ON DELETE CASCADE
    )
    """)

def delete_organizer(cursor, conn, uid):
    try:
        cursor.execute("SELECT COUNT(*) FROM Organizer WHERE uid = %s", (uid,))
        if cursor.fetchone()[0] == 0:
            print("Fail")
            return
        cursor.execute("DELETE FROM Organizer WHERE uid = %s", (uid,))
        conn.commit()
        print("Success")
    except Exception as e:
        print("Fail")

def reserve_slot(cursor, conn, eid, snum, uid):
    try:
        cursor.execute("""
            UPDATE Slot
            SET is_reserved = TRUE, uid = %s
            WHERE eid = %s AND snum = %s AND is_reserved = FALSE
        """, (uid, eid, snum))
        if cursor.rowcount == 1:
            conn.commit()
            print("Success")
        else:
            print("Fail")
    except Exception:
        print("Fail")

def cancel_reservation(cursor, conn, eid, snum, uid):
    try:
        cursor.execute("""
            UPDATE Slot
            SET is_reserved = FALSE, uid = NULL
            WHERE eid = %s AND snum = %s
              AND is_reserved = TRUE AND uid = %s
        """, (eid, snum, uid))
        if cursor.rowcount == 1:
            conn.commit()
            print("Success")
        else:
            print("Fail")
    except Exception:
        print("Fail")

def update_event(cursor, conn, eid, title, dt):
    try:
        cursor.execute("""
            UPDATE Event
            SET title = %s, datetime = %s
            WHERE eid = %s
        """, (title, dt, eid))
        if cursor.rowcount == 1:
            conn.commit()
            print("Success")
        else:
            print("Fail")
    except Exception:
        print("Fail")

def available_events(cursor, date):
    try:
        cursor.execute("""
            SELECT e.eid, e.title, e.type, e.datetime,
                   COUNT(*) AS availableSlots
            FROM Event e
            JOIN Slot s ON e.eid = s.eid
            WHERE s.is_reserved = FALSE
            AND e.datetime > %s
            GROUP BY e.eid, e.title, e.type, e.datetime
            ORDER BY e.datetime ASC, e.eid ASC
        """, (date,))
        rows = cursor.fetchall()
        for row in rows:
            print(','.join(str(x) for x in row))
    except Exception as e:
        print("Fail")

def popular_event_types(cursor, n):
    try:
        cursor.execute("""
            SELECT e.type, COUNT(*) AS reservedCount
            FROM Event e
            JOIN Slot s ON e.eid = s.eid
            WHERE s.is_reserved = TRUE
            GROUP BY e.type
            HAVING reservedCount >= %s
            ORDER BY reservedCount DESC, e.type ASC
        """, (n,))
        rows = cursor.fetchall()
        for row in rows:
            print(','.join(str(x) for x in row))
    except Exception as e:
        print("Fail")

def participant_schedule(cursor, uid):
    try:
        cursor.execute("""
            SELECT e.eid, e.title, e.type, e.datetime, s.snum,
                   v.vid, v.street, v.city, v.state, v.zip
            FROM Slot s
            JOIN Event e ON s.eid = e.eid
            LEFT JOIN Hosting h ON e.eid = h.eid AND h.is_primary = TRUE
            LEFT JOIN Venue v ON h.vid = v.vid
            WHERE s.uid = %s
            ORDER BY e.datetime ASC
        """, (uid,))
        rows = cursor.fetchall()
        for row in rows:
            print(','.join(str(x) if x is not None else 'NULL' for x in row))
    except Exception as e:
        print("Fail")


def organizer_event_count(cursor, n):
    try:
        cursor.execute("""
            SELECT o.uid, u.username, o.department, COUNT(*) AS eventCount
            FROM Organizer o
            JOIN User u ON o.uid = u.uid
            JOIN Event e ON o.uid = e.creator_uid
            GROUP BY o.uid, u.username, o.department
            HAVING eventCount >= %s
            ORDER BY eventCount DESC, o.uid ASC
        """, (n,))
        rows = cursor.fetchall()
        for row in rows:
            print(','.join(str(x) if x is not None else 'NULL' for x in row))
    except Exception as e:
        print("Fail")

def event_venues(cursor, vid):
    try:
        cursor.execute("""
            SELECT e.eid, e.title, e.type, e.datetime, h.is_primary
            FROM Hosting h
            JOIN Event e ON h.eid = e.eid
            WHERE h.vid = %s
            ORDER BY e.datetime ASC, e.eid ASC
        """, (vid,))
        rows = cursor.fetchall()
        for row in rows:
            print(','.join(str(x) if x is not None else 'NULL' for x in row))
    except Exception as e:
        print("Fail")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("function")
    parser.add_argument("args", nargs="*")

    args = parser.parse_args()

    conn = connect_db()
    cursor = conn.cursor()

    if args.function == "import":
        import_data(cursor, conn, args.args[0])
    else:
        cursor.execute("USE cs122a")
        if args.function == "insertAdmin":
            insert_admin(cursor, conn, int(args.args[0]), args.args[1], args.args[2], args.args[3], args.args[4], args.args[5])
        elif args.function == "addVenue":
            add_venue(cursor, conn, int(args.args[0]), int(args.args[1]), args.args[2].lower() == 'true')
        elif args.function == "deleteOrganizer":
            delete_organizer(cursor, conn, int(args.args[0]))
        elif args.function == "reserveSlot":
            reserve_slot(cursor, conn, int(args.args[0]), int(args.args[1]), int(args.args[2]))
        elif args.function == "cancelReservation":
            cancel_reservation(cursor, conn, int(args.args[0]), int(args.args[1]), int(args.args[2]))
        elif args.function == "updateEvent":
            update_event(cursor, conn, int(args.args[0]), args.args[1], args.args[2])
        elif args.function == "availableEvents":
            available_events(cursor, args.args[0])
        elif args.function == "popularEventTypes":
            popular_event_types(cursor, int(args.args[0]))
        elif args.function == "participantSchedule":
            participant_schedule(cursor, int(args.args[0]))
        elif args.function == "organizerStats":
            organizer_event_count(cursor, int(args.args[0]))
        elif args.function == "venueEvents":
            event_venues(cursor, int(args.args[0]))

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()