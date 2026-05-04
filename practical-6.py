# Practical 6: Flight and Cargo Scheduling Expert System

import datetime
import getpass
import hashlib
import os
import re
import secrets
import sqlite3


DB_FILE = "flight_schedule.db"
PLANES = 20

FLIGHTS = [
    (1, "Mumbai", 600, 149),
    (2, "Delhi", 900, 1400),
    (3, "Bangalore", 1130, 840),
    (4, "Chennai", 1400, 1100),
    (5, "Kolkata", 1615, 1900),
    (6, "Hyderabad", 730, 620),
    (7, "Goa", 815, 590),
    (8, "Ahmedabad", 1245, 530),
    (9, "Jaipur", 1430, 1200),
    (10, "Lucknow", 1700, 1450),
]

CARGO = [
    (1, "Medical Supplies", "Mumbai"),
    (2, "Auto Parts", "Delhi"),
    (3, "Electronics", "Bangalore"),
    (4, "Pharmaceuticals", "Chennai"),
    (5, "Textiles", "Kolkata"),
    (6, "IT Equipment", "Hyderabad"),
    (7, "Perishable Goods", "Goa"),
    (8, "Industrial Machinery", "Ahmedabad"),
    (9, "Gems and Jewellery", "Jaipur"),
    (10, "Agricultural Produce", "Lucknow"),
]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def heading(text):
    clear()
    print("=" * 60)
    print(text.center(60))
    print("=" * 60)


def ask(prompt, cast=str, default=None, valid=None):
    while True:
        hint = f" [{default}]" if default is not None else ""
        raw = input(f"{prompt}{hint}: ").strip()
        if not raw and default is not None:
            return default
        if not raw:
            print("Input required.")
            continue
        try:
            value = cast(raw)
        except ValueError:
            print("Invalid format.")
            continue
        if valid and not valid(value):
            print("Invalid value.")
            continue
        return value


def time_text(hhmm):
    return f"{hhmm // 100:02d}:{hhmm % 100:02d}"


def fuel_status(distance):
    fuel = distance * 0.3
    if fuel <= 800:
        return "OK", fuel
    if fuel <= 1000:
        return "CAUTION", fuel
    return "CRITICAL", fuel


def make_hash(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()


def setup_database(db):
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
        """
    )
    db.executescript(
        """
        DROP TABLE IF EXISTS flights;
        DROP TABLE IF EXISTS cargo;
        DROP TABLE IF EXISTS planes;

        CREATE TABLE flights (
            id INTEGER PRIMARY KEY,
            destination TEXT NOT NULL,
            time INTEGER NOT NULL,
            distance INTEGER NOT NULL,
            plane_id INTEGER
        );

        CREATE TABLE cargo (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            destination TEXT NOT NULL
        );

        CREATE TABLE planes (
            id INTEGER PRIMARY KEY,
            available INTEGER NOT NULL DEFAULT 1
        );
        """
    )
    db.executemany("INSERT INTO planes (id) VALUES (?)", [(i,) for i in range(1, PLANES + 1)])
    db.commit()


def first_free_plane(db):
    row = db.execute("SELECT id FROM planes WHERE available = 1 LIMIT 1").fetchone()
    if row:
        db.execute("UPDATE planes SET available = 0 WHERE id = ?", (row[0],))
        return row[0]
    return None


def add_flight(db, flight_id, destination, hhmm, distance, show=True):
    plane_id = first_free_plane(db)
    if plane_id is None:
        print("No plane is available.")
        return
    db.execute(
        "INSERT INTO flights VALUES (?, ?, ?, ?, ?)",
        (flight_id, destination, hhmm, distance, plane_id),
    )
    db.commit()
    if show:
        status, fuel = fuel_status(distance)
        print(f"Flight {flight_id} added. Plane {plane_id} assigned.")
        print(f"Fuel required: {fuel:.0f} units ({status})")


def seed_data(db):
    for row in FLIGHTS:
        add_flight(db, *row, show=False)
    db.executemany("INSERT INTO cargo VALUES (?, ?, ?)", CARGO)
    db.commit()


def sign_up(db):
    heading("Create Account")
    while True:
        username = ask("Username")
        if not re.fullmatch(r"[A-Za-z0-9_]{3,}", username):
            print("Use 3 or more letters, numbers, or underscores.")
            continue
        if db.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone():
            print("Username already exists.")
            continue
        break

    while True:
        password = getpass.getpass("Password: ")
        confirm = getpass.getpass("Confirm password: ")
        if len(password) < 6:
            print("Password must be at least 6 characters.")
        elif password != confirm:
            print("Passwords do not match.")
        else:
            break

    salt = secrets.token_hex(16)
    db.execute("INSERT INTO users VALUES (?, ?, ?)", (username, make_hash(password, salt), salt))
    db.commit()
    print(f"\nAccount created. Welcome, {username}!")
    pause()
    return username


def log_in(db):
    heading("Login")
    for attempt in range(3):
        username = ask("Username")
        password = getpass.getpass("Password: ")
        row = db.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,)).fetchone()
        if row and make_hash(password, row[1]) == row[0]:
            print(f"\nWelcome back, {username}!")
            pause()
            return username
        print(f"Invalid login. Attempts left: {2 - attempt}")
    pause()
    return None


def authenticate(db):
    while True:
        heading("Aviation Scheduling System")
        print("1. Login")
        print("2. Sign up")
        print("0. Exit")
        choice = ask("Choice", default="0")
        if choice == "1":
            user = log_in(db)
            if user:
                return user
        elif choice == "2":
            return sign_up(db)
        elif choice == "0":
            return None


def next_id(db, table):
    return (db.execute(f"SELECT MAX(id) FROM {table}").fetchone()[0] or 0) + 1


def print_rows(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))
    line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(line)
    print("-" * len(line))
    for row in rows:
        print("  ".join(str(value).ljust(widths[i]) for i, value in enumerate(row)))


def show_flights(db):
    heading("All Flights")
    rows = []
    for fid, dest, hhmm, distance, plane in db.execute(
        "SELECT id, destination, time, distance, plane_id FROM flights ORDER BY time"
    ):
        status, fuel = fuel_status(distance)
        rows.append((fid, dest, time_text(hhmm), distance, plane, f"{status} ({fuel:.0f})"))
    print_rows(("ID", "Destination", "Time", "KM", "Plane", "Fuel"), rows) if rows else print("No flights.")
    pause()


def show_schedule(db):
    heading("Flight-Cargo Schedule")
    rows = db.execute(
        """
        SELECT f.id, f.destination, f.time, c.id, c.name
        FROM flights f
        JOIN cargo c ON LOWER(f.destination) = LOWER(c.destination)
        ORDER BY f.time
        """
    ).fetchall()
    rows = [(f, d, time_text(t), c, n) for f, d, t, c, n in rows]
    print_rows(("Flight", "Destination", "Time", "Cargo ID", "Cargo"), rows) if rows else print("No matches.")
    pause()


def add_flight_ui(db):
    heading("Add Flight")
    fid = ask("Flight ID", int, next_id(db, "flights"), lambda x: x > 0)
    dest = ask("Destination")
    hhmm = ask("Departure time HHMM", int, valid=lambda x: 0 <= x <= 2359)
    distance = ask("Distance in km", int, valid=lambda x: x > 0)
    conflict = db.execute(
        "SELECT id, destination FROM flights WHERE ABS(time - ?) <= 30 LIMIT 1", (hhmm,)
    ).fetchone()
    if conflict:
        print(f"Warning: Flight {conflict[0]} to {conflict[1]} is within 30 minutes.")
        if ask("Add anyway? (y/n)", default="n").lower() != "y":
            print("Cancelled.")
            pause()
            return
    add_flight(db, fid, dest, hhmm, distance)
    pause()


def add_cargo_ui(db):
    heading("Add Cargo")
    cid = ask("Cargo ID", int, next_id(db, "cargo"), lambda x: x > 0)
    name = ask("Cargo name")
    dest = ask("Destination")
    db.execute("INSERT INTO cargo VALUES (?, ?, ?)", (cid, name, dest))
    db.commit()
    flight = db.execute(
        "SELECT id, time FROM flights WHERE LOWER(destination) = LOWER(?) ORDER BY time LIMIT 1",
        (dest,),
    ).fetchone()
    print(f"Cargo '{name}' added.")
    print(f"Matched with Flight {flight[0]} at {time_text(flight[1])}." if flight else "No matching flight yet.")
    pause()


def search(db, table):
    heading(f"Search {table.title()}")
    query = ask("Search text")
    if table == "flights":
        rows = db.execute(
            "SELECT id, destination, time FROM flights WHERE destination LIKE ? ORDER BY time",
            (f"%{query}%",),
        ).fetchall()
        rows = [(i, d, time_text(t)) for i, d, t in rows]
        headers = ("ID", "Destination", "Time")
    else:
        rows = db.execute(
            "SELECT id, name, destination FROM cargo WHERE name LIKE ? OR destination LIKE ?",
            (f"%{query}%", f"%{query}%"),
        ).fetchall()
        headers = ("ID", "Cargo", "Destination")
    print_rows(headers, rows) if rows else print("No records found.")
    pause()


def delete_flight(db):
    heading("Delete Flight")
    fid = ask("Flight ID", int, valid=lambda x: x > 0)
    row = db.execute("SELECT plane_id FROM flights WHERE id = ?", (fid,)).fetchone()
    if not row:
        print("Flight not found.")
    elif ask("Delete this flight? (y/n)", default="n").lower() == "y":
        db.execute("DELETE FROM flights WHERE id = ?", (fid,))
        db.execute("UPDATE planes SET available = 1 WHERE id = ?", (row[0],))
        db.commit()
        print("Flight deleted and plane released.")
    else:
        print("Cancelled.")
    pause()


def dashboard(db, username):
    now = datetime.datetime.now()
    current = now.hour * 100 + now.minute
    counts = (
        db.execute("SELECT COUNT(*) FROM flights").fetchone()[0],
        db.execute("SELECT COUNT(*) FROM cargo").fetchone()[0],
        db.execute("SELECT COUNT(*) FROM planes WHERE available = 1").fetchone()[0],
    )
    next_flight = db.execute(
        "SELECT id, destination, time FROM flights WHERE time >= ? ORDER BY time LIMIT 1",
        (current,),
    ).fetchone()
    print(f"Logged in as: {username}")
    print(f"Flights: {counts[0]} | Cargo: {counts[1]} | Free planes: {counts[2]}")
    if next_flight:
        print(f"Next: Flight {next_flight[0]} to {next_flight[1]} at {time_text(next_flight[2])}")
    print()


def main_menu(db, username):
    actions = {
        "1": add_flight_ui,
        "2": add_cargo_ui,
        "3": show_flights,
        "4": show_schedule,
        "5": lambda conn: search(conn, "flights"),
        "6": lambda conn: search(conn, "cargo"),
        "7": delete_flight,
    }
    while True:
        heading("Pune International Airport")
        dashboard(db, username)
        print("1. Add Flight")
        print("2. Add Cargo")
        print("3. Show All Flights")
        print("4. Show Flight-Cargo Schedule")
        print("5. Search Flights")
        print("6. Search Cargo")
        print("7. Delete Flight")
        print("0. Exit")
        choice = ask("Choice", default="0")
        if choice == "0":
            return
        actions.get(choice, lambda _: print("Invalid option."))(db)


def main():
    db = sqlite3.connect(DB_FILE)
    setup_database(db)
    seed_data(db)
    username = authenticate(db)
    if username:
        main_menu(db, username)
    db.close()


if __name__ == "__main__":
    main()