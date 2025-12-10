#! /usr/bin/env/ python3

from business import Battle
import db

#-------------------------------------------------------------------------


def main():

    db.welcome()        # Display the welcome screen
    db.display_Menu()   # Displays the menu
    print()

    battles = db.get_All_Battles()  # Loads all battle records from database

    while True:
        try:
            # Centers the menu option prompt
            menu_Option = db.get_Centered_Menu()
            print("-" * 226)

            if menu_Option == 1:
                db.display_All_Battles(battles) # Displays details of all battles
            elif menu_Option == 2:
                db.add_Battle(battles)          # Prompts user for details and adds new battle
            elif menu_Option == 3:
                db.edit_Battle(battles)         # Allows user to select and edit attributes of battle
            elif menu_Option == 4:
                db.delete_Battle(battles)       # Allows user to select and delete battle
            elif menu_Option == 5:
                db.sort_Battles(battles)        # Sorts and displays battles from oldest to newest
            elif menu_Option == 6:
                db.sort_Battles_Desc(battles)   # Sorts and displays battles from newest to oldest
            elif menu_Option == 7:
                found_Battle = db.look_Up_Battle(battles)   # Searches specific battle by name
                if found_Battle:                            # If battle is found then it's details are printed
                    print("-" * 226)
                    print(db.get_Centered_String("BATTLE DETAILS"))
                    print()
                    print("Battle Name: " + found_Battle.battleName)
                    print("\nDate: " + found_Battle.date.isoformat())
                    print("\nCountries Involved: " + found_Battle.countriesInvolved)
                    print("\nWinner: " + found_Battle.winner)
                    print("\nLoser: " + found_Battle.loser)
                    print("\nVictor Forces: " + str(found_Battle.victorForces))
                    print("\nVanquished Forces: " + str(found_Battle.vanquishedForces))
                    print("\nTotal Victor Deaths: " + str(found_Battle.totalVictorDeaths))
                    print("\nTotal Vanquished Deaths: " + str(found_Battle.totalVanquishedDeaths))
                    print("\nSignificant Figures Present:\n" + found_Battle.significantFiguresPresent)
                    print("\nNotable Deaths:\n" + found_Battle.notableDeaths)
                    print()
                    print("=" * 226)
            elif menu_Option == 8:
                db.calculate_Time_Diff(battles) # Calculates and displays time elapsed since chosen battle.
            elif menu_Option == 9:
                db.display_Menu()               # Displays the menu for convenience
            elif menu_Option == 10:              # Exits loop
                print(db.get_Centered_String("Initiating program exit... Program now terminated."))
                break
            else:
                print("Entry not valid. Please choose a menu option.")


        except Exception as e:
            print(f"\nAn unexpected error occurred: {e!s}")
            print("Please select a menu option again.")

if __name__ == "__main__":
    main()
                
                




