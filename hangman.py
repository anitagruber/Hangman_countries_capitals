import os
import random
import wordlist
import findchar


# ---- ASCII akasztófa állapotok ----
HANGMAN_PICS = [
    r"""
     +---+
         |
         |
         |
        ===""",
    r"""
     +---+
     O   |
         |
         |
        ===""",
    r"""
     +---+
     O   |
     |   |
         |
        ===""",
    r"""
     +---+
     O   |
    /|   |
         |
        ===""",
    r"""
     +---+
     O   |
    /|\  |
         |
        ===""",
    r"""
     +---+
     O   |
    /|\  |
    /    |
        ===""",
    r"""
     +---+
     O   |
    /|\  |
    / \  |
        ==="""
]

# ---- globális nehézség ----
difficulty = "medium"   # alapértelmezett


def set_difficulty():
    """Nehézség beállítása: easy / medium / hard (csak szöveges menü)."""
    global difficulty

    while True:
        os.system("cls")
        print("    ==== NEHÉZSÉG ====")
        print("Jelenlegi nehézség:", difficulty.upper())
        print("----------------------------")
        print("  1) EASY    (7 élet)")
        print("  2) MEDIUM  (5 élet)")
        print("  3) HARD    (3 élet)")
        print("  4) Vissza a menübe")
        print("----------------------------")

        choice = input("Válassz: ")

        if choice == "1":
            difficulty = "easy"
            print("\nNehézség beállítva: EASY")
            input("Nyomj Entert a visszalépéshez...")
            return
        elif choice == "2":
            difficulty = "medium"
            print("\nNehézség beállítva: MEDIUM")
            input("Nyomj Entert a visszalépéshez...")
            return
        elif choice == "3":
            difficulty = "hard"
            print("\nNehézség beállítva: HARD")
            input("Nyomj Entert a visszalépéshez...")
            return
        elif choice == "4":
            return
        else:
            print("Érvénytelen választás!")
            input("Nyomj Entert...")


def play_game():
    """Egy teljes Hangman játék lefuttatása ország–főváros módban."""
    global difficulty

    # --- ország + főváros választása nehézség szerint ---
    if difficulty == "easy":
        country, wd = random.choice(wordlist.pairs_easy)
    elif difficulty == "medium":
        country, wd = random.choice(wordlist.pairs_medium)
    else:
        country, wd = random.choice(wordlist.pairs_hard)

    # --- maszkolt főváros ---
    mk = "_" * len(wd)

    # speciális karakterek felfedése (szóköz, kötőjel stb.)
    specials = [" ", "_", "-", "'", "/", ","]
    for s in specials:
        mk = findchar.find_char(wd, mk, s)

    # --- életek száma nehézség alapján ---
    if difficulty == "easy":
        lives = 7
    elif difficulty == "medium":
        lives = 5
    else:
        lives = 3

    starting_lives = lives

    guessed_letters = set()
    wrong_letters = set()

    os.system("cls")

    print(HANGMAN_PICS[0])
    print()
    
    print(f"Ország: {country}")
    print("A főváros:", mk)
    print(f"Életek: {lives}")

    # --- játék ciklus ---
    while mk != wd and lives > 0:
        char = input("Írj be egy karaktert (vagy 'quit' a kilépéshez): ")

        # kilépés a játékból
        if char.lower() == "quit":
            print("Kiléptél a játékból. Viszlát!")
            return  # kilépünk a play_game-ből

        # csak 1 karakter legyen
        if len(char) != 1:
            print("Csak egy karaktert írj!")
            continue

        # ismételt tipp
        if char.lower() in guessed_letters:
            print("Ezt a betűt már próbáltad, válassz másikat!")
            continue

        # új tipp eltárolása
        guessed_letters.add(char.lower())

        # rossz tipp: élet levonás + hibás betűk bővítése
        if char.lower() not in wd.lower():
            lives -= 1
            wrong_letters.add(char.lower())

        # maszk frissítése
        mk = findchar.find_char(wd, mk, char)

        # képernyő törlése
        os.system("cls")

        # ASCII akasztófa skálázva az életekhez
        lost_lives = starting_lives - lives
        if lost_lives < 0:
            lost_lives = 0
        if lost_lives > starting_lives:
            lost_lives = starting_lives

        max_stage = len(HANGMAN_PICS) - 1
        progress_ratio = lost_lives / starting_lives  # 0.0 .. 1.0
        index = int(progress_ratio * max_stage)
        if index < 0:
            index = 0
        if index > max_stage:
            index = max_stage

        print(HANGMAN_PICS[index])
        print()

        # állapot kiírása
        print(f"Ország: {country}")
        print("A főváros:", mk)
        print(f"Életek: {lives}")
        print("Összes tipp:", ", ".join(sorted(guessed_letters)))
        if wrong_letters:
            print("Rossz tippek:", ", ".join(sorted(wrong_letters)))
        else:
            print("Rossz tippek: -")

    # --- játék vége ---
    os.system("cls")

    if mk == wd:
        # WIN képernyő
        print("\033[92m" + r"""
  ██╗    ██╗██╗███╗   ██╗
  ██║    ██║██║████╗  ██║
  ██║ █╗ ██║██║██╔██╗ ██║
  ██║███╗██║██║██║╚██╗██║
  ╚███╔███╔╝██║██║ ╚████║
   ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝
        """ + "\033[0m")
        print(f"\nA megoldás: {wd} ({country})")
        
    else:
        # GAME OVER képernyő
        print("\033[91m" + r"""
  ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ 
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
 ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██║   ██║██╔══╝  ██╔══██╗
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝╚██████╔╝███████╗██║  ██║
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
        """ + "\033[0m")
        print(f"\nA megoldás az alábbi volt: {wd} ({country})")
        

    input("\nNyomj Entert a főmenühöz...")

def main_menu():
    """Főmenü: Play / Difficulty / Exit, ASCII logóval."""
    while True:
        os.system("cls")

        print("\033[93m" + r"""
       ███╗   ███╗███████╗███╗   ██╗██╗   ██╗
       ████╗ ████║██╔════╝████╗  ██║██║   ██║
       ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║
       ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║
       ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝
       ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝
        """ + "\033[0m")

        print("                  \033[93m★\033[0m  HANGMAN  \033[93m★\033[0m")
        print("--------------------------------------------------")
        print(f"  Jelenlegi nehézség: {difficulty.upper()}")
        print("--------------------------------------------------")
        print("  1) Játék")
        print("  2) Nehézség")
        print("  3) Kilépés")
        print("--------------------------------------------------")

        choice = input("Válassz: ")

        if choice == "1":
            play_game()
        elif choice == "2":
            set_difficulty()
        elif choice == "3":
            print("Viszlát!")
            break
        else:
            print("Érvénytelen opció!")
            input("Nyomj Entert...")


if __name__ == "__main__":
    main_menu()