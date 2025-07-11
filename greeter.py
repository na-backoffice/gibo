import sys
from datetime import datetime

def begruessen(name="Fremder"):
    stunde = datetime.now().hour
    if 5 <= stunde < 12:
        teil = "Morgen"
    elif 12 <= stunde < 18:
        teil = "Nachmittag"
    else:
        teil = "Abend"
    print(f"\033[1;36mGuten {teil}, {name}! Willkommen in deiner Kommandozeile.\033[0m")

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else None
    begruessen(name)