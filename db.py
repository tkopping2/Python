#! /usr/bin/env/ python3

import sqlite3
from contextlib import closing

from business import Battle
from datetime import date,datetime

# Global constant for formating
TARGET_WIDTH = 226

conn = None

#-------------------------------------------------------------------------

# Establishes a connection to the sqlite database file if one doesn't already exist
def connect():
    global conn
    if not conn:
        DB_FILE = "Final.sqlite"
        conn = sqlite3.connect(DB_FILE)
        # Allows access to columns by name
        conn.row_factory = sqlite3.Row

#-------------------------------------------------------------------------

# Inserts new battle into the battles table
# battle_obj is the battle object containing the data to be saved
def insert_Battle(battle_obj):
    
    connect()
    global conn
    
    sql = '''
    INSERT INTO battles (
        battleName, date, countriesInvolved, winner, loser, victorForces,
        vanquishedForces, totalVictorDeaths, totalVanquishedDeaths,
        significantFiguresPresent, notableDeaths
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Tuple of values from the Battle object to match the SQL query
    values = (
        battle_obj.battleName,
        battle_obj.date.isoformat(), # Converts date object to YYYY-MM-DD
        battle_obj.countriesInvolved,
        battle_obj.winner,
        battle_obj.loser,
        battle_obj.victorForces,
        battle_obj.vanquishedForces,
        battle_obj.totalVictorDeaths,
        battle_obj.totalVanquishedDeaths,
        battle_obj.significantFiguresPresent,
        battle_obj.notableDeaths
    )
    # Use closing for cursor to ensure release of database resources
    with closing(conn.cursor()) as c:
        c.execute(sql, values)
        # Retrieves auto-generated primary key and assigns it back to the program
        battle_obj.db_id = c.lastrowid
        # Commits the transaction
        conn.commit()
        
#-------------------------------------------------------------------------

# Updates an existing Battle's data in the 'battles' table based on its 'db_id'
def update_Battle(battle_obj):
    connect()
    global conn
    
    # Ensures the object has a database id before attempting an update.
    # First part checks object for id and the second part
    # only works if the battle_obj has the id
    if not hasattr(battle_obj, 'db_id') or battle_obj.db_id is None:
        return

    # Query to update all columns using the id column in the WHERE clause
    sql = '''
            UPDATE battles SET
                battleName = ?, date = ?, countriesInvolved = ?, winner = ?,
                loser = ?, victorForces = ?, vanquishedForces = ?,
                totalVictorDeaths = ?, totalVanquishedDeaths = ?,
                significantFiguresPresent = ?, notableDeaths = ?
            WHERE id = ?
            '''

    values = (
        battle_obj.battleName,
        battle_obj.date.isoformat(),
        battle_obj.countriesInvolved,
        battle_obj.winner,
        battle_obj.loser,
        battle_obj.victorForces,
        battle_obj.vanquishedForces,
        battle_obj.totalVictorDeaths,
        battle_obj.totalVanquishedDeaths,
        battle_obj.significantFiguresPresent,
        battle_obj.notableDeaths,
        battle_obj.db_id # Used to identify the exact row to update
    )

    with closing(conn.cursor()) as c:
        c.execute(sql, values)
        conn.commit()

#-------------------------------------------------------------------------

# Retrieves all records from the 'battles' table and converts into list of Battle objects.
# Returns a list of Battle objects
def get_All_Battles() -> list[Battle]:
    connect()
    global conn

    # Query to select necessary columns
    query = '''
    SELECT id, battleName, date, countriesInvolved, winner, loser,
        victorForces, vanquishedForces, totalVictorDeaths,
        totalVanquishedDeaths, significantFiguresPresent, notableDeaths
    FROM battles
    '''

    battles = []

    with closing(conn.cursor()) as c:
        c.execute(query)
        rows = c.fetchall() # Fetches all matching rows from database

        for row in rows:

            # Converts the date string into Python date object
            battle_date = datetime.strptime(row['date'], '%Y-%m-%d').date()

            # Creates new Battle object using data from the database row
            new_Battle = Battle(
                battleName=row['battleName'],
                date=battle_date,
                countriesInvolved=row['countriesInvolved'],
                winner=row['winner'],
                loser=row['loser'],
                # Convert into Python integers for death counts
                victorForces=int(row["victorForces"]),
                vanquishedForces=int(row['vanquishedForces']),
                totalVictorDeaths=int(row['totalVictorDeaths']),
                totalVanquishedDeaths=int(row['totalVanquishedDeaths']),
                significantFiguresPresent=row['significantFiguresPresent'],
                notableDeaths=row['notableDeaths']
            )

            new_Battle.db_id = row['id']
                    
            battles.append(new_Battle)
                    
    return battles

#-------------------------------------------------------------------------

# Prints formatted list of battle records
def display_All_Battles(battles: list[Battle]):

    print()
    print(get_Centered_String("BATTLE RECORDS\n"))
    

    if not battles:
        print("\nNo battles recorded.")
        return

    # Defines the formatting for the main header and rows
    core_Header_Format = (
        "{:<11} "
        "{:<36} "
        "{:<36} "
        "{:<42} "
        "{:<22} "
        "{:>25} "
        "{:>37} "

    )

    HEADER_WIDTH = 226
    print("=" * HEADER_WIDTH)
    print(core_Header_Format.format(
        "ID",
        "BATTLE NAME",
        "DATE OF BATTLE",
        "COUNTRIES INVOLVED",
        "VIC. FORCES",
        "VANQ. FORCES",
        "TOTAL DEATHS",
    
    ))

    # Loops through the list of battles for display
    for i, battle in enumerate(battles, 1):

        # Creates the formatted row output for the current battle
        core_Row_Output = core_Header_Format.format(
            i,
            battle.battleName,
            battle.date.isoformat(),
            battle.countriesInvolved,
            f"{battle.victorForces:,}",
            f"{battle.vanquishedForces:,}",
            f"{battle.total_Deaths:,}"
        )
        print("-" * HEADER_WIDTH)
        
        print(core_Row_Output)

        print("-" * HEADER_WIDTH)

        # Prints information below the main table row
        # I did this because it looks more organized and improves readability
        if battle.winner and battle.loser:
            print(f"\nWINNER/LOSER: {battle.winner} vs {battle.loser}")

        if battle.totalVictorDeaths:
            print(f"\nTotal Deaths of {battle.winner}: {battle.totalVictorDeaths}")

        if battle.totalVanquishedDeaths:
            print(f"\nTotal Deaths of {battle.loser}: {battle.totalVanquishedDeaths}")

        if battle.significantFiguresPresent:
            print(f"\nFIGURES PRESENT: \n{battle.significantFiguresPresent}")

        if battle.significantFiguresPresent:
            print(f"\nNOTABLE DEATHS: \n{battle.notableDeaths}")
            print()


    print("=" * HEADER_WIDTH)

#-------------------------------------------------------------------------
    
# Prompts the user for details to create a new battle object and save it to the database
def add_Battle(battles: list[Battle]):

    print("\n")
    print(get_Centered_String("ADD NEW BATTLE"))
    print("-" * TARGET_WIDTH) # This is where the TARGET_WIDTH variable comes in handy
    print()

    # Takes the user input and converts it to Title Case
    # Ensures all input will match name if spelled correctly
    battleName = input("Battle Name: ").title()

    print()

    battle_Date = get_Date()
    
    countriesInvolved = input("\nCountries Involved: ")
    # Converts winner and loser input to Title Case
    winner = input("\nWinner: ").title()
    loser = input("\nLoser: ").title()

    # get_Valid_Int function is used to validate and get integer inputs
    victorForces = get_Valid_Int("\nVictor Forces: ")
    vanquishedForces = get_Valid_Int("\nVanquished Forces: ")
    totalVictorDeaths = get_Valid_Int("\nTotal Victor Deaths: ")
    totalVanquishedDeaths = get_Valid_Int("\nTotal Vanquished Deaths: ")
    significantFiguresPresent = input("\nSignificant Figures Present: ")
    notableDeaths = input("\nNotable Deaths: ")

    # Creates the new Battle object
    new_Battle = Battle(
        battleName=battleName,
        date=battle_Date,
        countriesInvolved=countriesInvolved,
        winner=winner,
        loser=loser,
        victorForces=victorForces,
        vanquishedForces=vanquishedForces,
        totalVictorDeaths=totalVictorDeaths,
        totalVanquishedDeaths=totalVanquishedDeaths,
        significantFiguresPresent=significantFiguresPresent,
        notableDeaths=notableDeaths
    )


    battles.append(new_Battle)

    # Saves the object to the database
    insert_Battle(new_Battle)

    print("\nBattle successfully added to the list!")
    print(f"\nTotal battles saved: {len(battles)}")

#-------------------------------------------------------------------------

# Allows user to look up battle and delete it from database
def delete_Battle(battles: list[Battle]):
    
    print()
    print(get_Centered_String("DELETE BATTLE"))

    battle_To_Delete = look_Up_Battle(battles)

    if battle_To_Delete is None:
        return

    print(f"\nAre you sure you want to delete the Battle of {battle_To_Delete.battleName}?\n")
    confirmation = input("1 - Yes\n2 - No\n\nEnter: ")

    
    if confirmation == '1':

        # Checks if object has a database id hasattr = has attribute
        if hasattr(battle_To_Delete, 'db_id') and battle_To_Delete.db_id is not None:
            connect()
            global conn

            with closing(conn.cursor()) as c:
                # Executes the DELETE command using battle's db_id
                c.execute("DELETE FROM battles WHERE id = ?", (battle_To_Delete.db_id,))
                conn.commit()
            
            try:
                # Removes object
                battles.remove(battle_To_Delete)
                print(f"\nSuccessfully deleted the Battle of {battle_To_Delete.battleName}.")

            except ValueError:
                print("\nError: Could not find battle in the battle list.")

        else:
            # If no db_id is present
            try:
                battles.remove(battle_To_Delete)
                print(f"\nSuccessfully deleted the Battle of {battle_To_Delete.battleName}.")

            except ValueError:
                print("\nError: Could not find battle in the battle list.")
                
    elif confirmation == '2':
        print("\nDeletion Cancelled.")
    else:
        print("\nInvalid Choice. Deletion Cancelled.")

    print("-" * TARGET_WIDTH)

#-------------------------------------------------------------------------

# Prompts user for battle name and then searches for a matching battle name
def look_Up_Battle(battles: list[Battle]):
    

    VISUAL_SHIFT = " " * 99
    prompt_Text = "Enter name of battle: "

    print()

    print(VISUAL_SHIFT + prompt_Text, end="")

    # Takes input and converts to Title Case
    # Ensures all input will match name if spelled correctly
    user_Input = input().title()
    name = user_Input

    # Generator expression to look through each row and find first battle name match
    found_Battle = next((b for b in battles if b.battleName.title() == name.title()), None)

    if found_Battle is None:
        error_Message = f"Error: Battle '{name}' not found." 
        print("\n" + VISUAL_SHIFT + error_Message)
        return None

    return found_Battle

#-------------------------------------------------------------------------

# Allows user to edit attributes of chosen battle
# This will repeat until user chooses to exit (0)
def edit_Battle(battles: list[Battle]):

    print("\n")
    print(get_Centered_String("EDIT BATTLE"))
    print("-" * 226)

    # Searches the battle to be edited
    battle_To_Edit = look_Up_Battle(battles)
    if battle_To_Edit is None:
        return

    # This loop allows the user to make multiple changes without having to repeatedly select
    # the 'Edit Battle' menu option and search for the battle
    while True:

        print()

        print("CURRENT BATTLE DATA\n")

        # Displays current battle data of battle being edited
        print("Battle Name: " + battle_To_Edit.battleName)
        print("Date: " + battle_To_Edit.date.isoformat())
        print("Countries Involved: " + battle_To_Edit.countriesInvolved)
        print("Winner: " + battle_To_Edit.winner)
        print("Loser: " + battle_To_Edit.loser)
        print("Victor Forces: " + str(battle_To_Edit.victorForces))
        print("Vanquished Forces: " + str(battle_To_Edit.vanquishedForces))
        print("Total Victor Deaths: " + str(battle_To_Edit.totalVictorDeaths))
        print("Total Vanquished Deaths: " + str(battle_To_Edit.totalVanquishedDeaths))
        print("\nSignificant Figures Present: " + battle_To_Edit.significantFiguresPresent)
        print("\nNotable Deaths: " + battle_To_Edit.notableDeaths)

        print("-" * 226)

        print("\nWhich attribute would you like to edit?\n")
        print(" 1. Battle Name")
        print(" 2. Date")
        print(" 3. Countries Involved")
        print(" 4. Winner")
        print(" 5. Loser")
        print(" 6. Victor Forces")
        print(" 7. Vanquished Forces")
        print(" 8. Total Victor Deaths")
        print(" 9. Total Vanquished Deaths")
        print("10. Significant Figures Present")
        print("11. Notable Deaths\n")
        print()

        try:
            choice = int(input("Enter number to edit or 0 to finish editing: "))
            print()
        except ValueError:
            print("Invalid input. Returning to main menu.")
            display_Menu()
            break

        # Dictionary of menu number that corresponds with the attribute name
        attr_Map = {
            1: 'battleName', 2: 'date', 3: 'countriesInvolved', 4: 'winner',
            5: 'loser', 6: 'victorForces', 7: 'vanquishedForces',
            8: 'totalVictorDeaths', 9: 'totalVanquishedDeaths',
            10: 'significantFiguresPresent', 11: 'notableDeaths'
        }

        if choice == 0:
            print("Edit finished. Returning to menu.")
            display_Menu()
            break # Exits loop

        attribute_Name = attr_Map.get(choice)

        if attribute_Name is None:
            print("Invalid option number. Please try again.")
            continue # Restarts loop

        # Input validation and conversion
        if attribute_Name == 'date':
            new_Value = get_Date()

        elif attribute_Name in ['victorForces', 'vanquishedForces', 'totalVictorDeaths', 'totalVanquishedDeaths']:
            new_Value = get_Valid_Int(f"Enter new value for {attribute_Name}: ")

        else:
            prompt = f"\nEnter new value for {attribute_Name}: "
            new_Value = input(prompt)

            # Converts these field names to Title Case
            if attribute_Name in ['battleName', 'winner', 'loser']:
                new_Value = new_Value.title()

        # Updates the attribute on the battle object
        setattr(battle_To_Edit, attribute_Name, new_Value)

        # Saves the change to the database
        update_Battle(battle_To_Edit)

        print(f"\nSuccessfully updated '{attribute_Name}'.")
        print(f"\nNew value: {new_Value}\n")

#-------------------------------------------------------------------------

# Sorts the list of battles by date from oldest to newest and displays them
def sort_Battles(battles: list[Battle]):

    print()

    NAME_W = 50
    DATE_W = 25

    TABLE_WIDTH = NAME_W + 1 + DATE_W + 1

    padding = " " * ((TARGET_WIDTH - TABLE_WIDTH) // 2)

    title = "Battles - Oldest to Most Recent"

    print("\n" + get_Centered_String(title))
    print("\n")

    if not battles:
        print(padding + "No battles recorded to sort.")
        return

    # Sorts the list by the date attribute using lambda function shortcut
    # Basically tells the sorted() function what to sort by
    # the sorted() function sorts in ASC order by default
    sorted_Battles = sorted(battles, key=lambda battle: battle.date)


    FIRST_COL_TOTAL_W = len(padding) + DATE_W

    # Formatting for the table header and rows
    header_Format = "{:<" + str(NAME_W) + "} {:<" + str(DATE_W) + "}"

    print("=" * 226)
    print(header_Format.format("BATTLE NAME", "DATE"))
    print("-" * 226)
    
    for i, battle in enumerate(sorted_Battles, 1):
        print(header_Format.format(
            battle.battleName,
            battle.date.isoformat()
        ))
        
    print()

#-------------------------------------------------------------------------

# Sorts the list of battles by date from newest to oldest and displays them
def sort_Battles_Desc(battles: list[Battle]):

    print()

    NAME_W = 50
    DATE_W = 25

    TABLE_WIDTH = NAME_W + 1 + DATE_W + 1

    padding = " " * ((TARGET_WIDTH - TABLE_WIDTH) // 2)

    title = "Battles - Most Recent to Oldest"

    print("\n" + get_Centered_String(title))
    print("\n")

    if not battles:
        print(padding + "No battles recorded to sort.")
        return

    # Sorts the list by the date attribute using lambda function shortcut
    # Basically tells the sorted() function what to sort by and then reverse it
    # since the sorted() function sorts in ASC by default.
    sorted_Battles = sorted(battles, key=lambda battle: battle.date, reverse=True)

    # Formatting for the table header and rows
    header_Format = "{:<" + str(NAME_W) + "} {:<" + str(DATE_W) + "}"

    print("=" * TARGET_WIDTH)
    print(header_Format.format("BATTLE NAME", "DATE"))
    print("-" * TARGET_WIDTH)
    
    for i, battle in enumerate(sorted_Battles, 1):
        print(header_Format.format(
            battle.battleName,
            battle.date.isoformat()
        ))
        
    print()

#-------------------------------------------------------------------------

# Prompts user for battle and calculates the time elapsed since
def calculate_Time_Diff(battles: list[Battle]):
    print("\n")

    print(get_Centered_String("Time since this battle occurred."))

    print("-" * 226)

    # Looks up the battle the user wants
    battle_Chosen = look_Up_Battle(battles)
    if battle_Chosen is None:
        return

    today = date.today()

    # Calculates the time_Past object
    time_Past = today - battle_Chosen.date
    
    print()

    print(f"BATTLE NAME: {battle_Chosen.battleName}\n")
    print(f"BATTLE DATE: {battle_Chosen.date.isoformat()}\n")
    print(f"TODAY'S DATE: {today.isoformat()}\n")

    # Calculates years and remaining days
    # From what I've gathered using 365.25 is a slightly more accurate estimate for older battles.
    years = time_Past.days // 365.25
    remaining_Days = time_Past.days % 365   # Modulo operator to get remaining days.

    print(f"TIME ELAPSED: {years} years and {remaining_Days} days.")
    print()
    print("-" * 226)
        


#-------------------------------------------------------------------------   

# Prompts user for date string and validate against YYYY-MM-DD
def get_Date():

    # Uses lognest text to find len and use it for a padding variable for centering
    padding = get_Padding(len("Error: The date was entered in the wrong format. Please use YYYY-MM-DD."))
    
    while True:
        date_str = input("Date of Battle YYYY-MM-DD: ")
        try:
            # Parse the string into a datetime object
            battle_Date = datetime.strptime(date_str, '%Y-%m-%d').date()

            return battle_Date

        except ValueError:
            print(padding + "Error: The date was entered in the wrong format. Please use YYYY-MM-DD.")

#-------------------------------------------------------------------------

# Prompts user for input and returns a valid non-negative integer
def get_Valid_Int(prompt: str) -> int:

    one_Padding = get_Padding(len("Value must be zero or greater."))
    two_Padding = get_Padding(len("Invalid input. Please enter a whole number."))

    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            else:
                print(one_Padding + "Value must be zero or greater.")
        except ValueError:
            print(two_Padding + "Invalid input. Please enter a whole number.")

#-------------------------------------------------------------------------
    


#-------------------------------------------------------------------------

# Prints the current date in the specified format
def display_Date():
    date_Format = "%Y-%m-%d"
    now = datetime.now()
    current_Date = datetime(now.year, now.month, now.day)
    print(f"Today's Date: {current_Date.strftime(date_Format)}")

#-------------------------------------------------------------------------

# Prints the main menu options and centers them based on the TARGET_WIDTH
def display_Menu():
    TARGET_WIDTH = 226

    # Calculates padding
    LONGEST_LINE_LENGTH = len("4 - Show Battles From Oldest to Most Recent")

    padding = " " * ((TARGET_WIDTH - LONGEST_LINE_LENGTH) // 2)

    HEADER_SEPARATOR_LENGTH = len("BATTLE MANAGER")
    header_Padding = " " * ((TARGET_WIDTH - HEADER_SEPARATOR_LENGTH) // 2)

    MESSAGE_SEPARATOR_LENGTH = len("Select an Option!")
    message_Padding = " " * ((TARGET_WIDTH - MESSAGE_SEPARATOR_LENGTH) // 2)

    SAVE_MESSAGE_LENGTH = len("----------All records will be saved upon exiting the program----------")
    save_Message_Padding = " " * ((TARGET_WIDTH - SAVE_MESSAGE_LENGTH) // 2)

    print("=" * 226)
    print()
    # Prints Header
    print(header_Padding + "BATTLE MANAGER")
    print(padding)
    # Prints all menu options
    print(padding + " 1 - Display All Battles")
    print(padding + " 2 - Add Battle")
    print(padding + " 3 - Edit Battle")
    print(padding + " 4 - Delete Battle")
    print(padding + " 5 - Show Battles from Oldest to Most Recent")
    print(padding + " 6 - Show Battles from Most Recent to Oldest")
    print(padding + " 7 - Look up Battle")
    print(padding + " 8 - Time Since Battle Occurred")
    print(padding + " 9 - Display Menu")
    print(padding + "10 - Exit")
    print()
    print()

    print(save_Message_Padding + "----------All records will be saved upon exiting the program----------")

    print()

    print(message_Padding + "Select an Option!")
    print()


#-------------------------------------------------------------------------

# Prints initial welcome screen that comes before the main program
def welcome():
    print()
    print("=" * 226)
    print()
    print(f"{'WELCOME TO THE BATTLE MANAGER':^226}")
    print()
    print("-" * 226)
    print()

    input(f"{'Press ENTER to witness history!':^226}")
    print()

#-------------------------------------------------------------------------

# Prompts the user for a menu option and makes sure it is centered
def get_Centered_Menu() -> int:

    PROMPT_LENGTH = len("Menu Option: ")
    prompt_Padding = " " * ((TARGET_WIDTH - PROMPT_LENGTH) // 2)

    try:
        # Gets input and converts it to an integer
        return int(input(prompt_Padding + "Menu Option: "))

    except ValueError:
        raise ValueError("Input must be a valid number.")


#-------------------------------------------------------------------------

# Calculates the spaces needed to center text
def get_Padding(text_Length: int) -> str:
    return " " * ((TARGET_WIDTH - text_Length) // 2)

# Centers the given text string
def get_Centered_String(text: str) -> str:
    return text.center(TARGET_WIDTH)

#-------------------------------------------------------------------------



