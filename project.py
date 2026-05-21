

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




def connect_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
        )
    return mydb


def create_tables(cursor):
    cursor.execute("DROP DATABASE IF EXISTS cs122a_hw2")
    cursor.execute("CREATE DATABASE cs122a_hw2")
    cursor.execute("USE cs122a_hw2")

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



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("function")
    parser.add_argument("args", nargs="*")

    args = parser.parse_args()


    conn = connect_db()
    cursor = conn.cursor()
    
    create_tables(cursor)
    
    if(args.function == "import"):
        pass 

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
