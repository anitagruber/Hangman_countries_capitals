import os

pairs_easy = []
pairs_medium = []
pairs_hard = []



def load_countries_and_capitals():
    # annak a mappának az elérési útja, ahol a wordlist.py van
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(base_dir, "countries-and-capitals.txt")

    if not os.path.exists(filename):
        print(f" A fájl nem található itt: {filename}")
        return

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split("|")
            if len(parts) != 2:
                continue

            country = parts[0].strip()
            city = parts[1].strip()

            # város hossz számítása (szóköz nélkül)
            length = len(city.replace(" ", ""))

            # nehézség kategorizálása
            if length <= 6:
                pairs_easy.append((country, city))
            elif length <= 10:
                pairs_medium.append((country, city))
            else:
                pairs_hard.append((country, city))

# modul betöltésekor fusson le
load_countries_and_capitals()