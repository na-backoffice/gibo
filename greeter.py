import sys
from datetime import datetime

def greet(name="Stranger"):
    hour = datetime.now().hour
    if 5 <= hour < 12:
        part = "morning"
    elif 12 <= hour < 18:
        part = "afternoon"
    else:
        part = "evening"
    print(f"\033[1;36mGood {part}, {name}! Welcome to your command line.\033[0m")

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else None
    greet(name)