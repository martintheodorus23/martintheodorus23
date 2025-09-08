import random as rm
import time
import webbrowser
from datetime import datetime

# sensors 

import time

def get_day_period():
    current_time = time.ctime()
    hour = int(current_time.split()[3].split(":")[0])
    
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"

def get_weekday_type():
    weekday = time.ctime().split()[0]  # e.g. "Mon"
    return "weekend" if weekday in ["Sat", "Sun"] else "weekday"

def get_day_part_status():
    hour = int(time.ctime().split()[3].split(":")[0])
    return "work hours" if 9 <= hour < 18 else "rest hours"

# actuators

actions = [
    lambda: print("I am working..."),
    lambda: print("ok"),
    lambda: print("The current time is", datetime.now().strftime("%H:%M:%S")),
    lambda: print("Today is", datetime.now().strftime("%A, %d %B %Y")),
    lambda: (print("Opening Google..."), webbrowser.open("https://www.google.com")),
    lambda: print("🚀 Keep going Martin, you’re building the future!"),
    lambda: (lambda a, b: print(f"{a} + {b} = {a+b}"))(rm.randint(1, 10), rm.randint(1, 10)),
]

mind = {}

while True:
    sit = '$'.join([
        get_day_period(),
        get_weekday_type(),
        get_day_part_status()
    ])

    if sit not in mind:
        mind[sit] = [1] * len(actions)
        
    act = rm.choices(actions, mind[sit], k=1)[0]

    print(f"Situation: {sit} -> Action: {actions.index(act)}")
    act()

    # --- feedback mechanism ---
    idx = actions.index(act)
    if "work hours" in sit and idx in [0, 2, 3]:  
        mind[sit][idx] += 1   # reward productive actions in work hours
    elif "rest hours" in sit and idx in [5, 6]:  
        mind[sit][idx] += 1   # reward fun/encouraging actions in rest hours
    else:
        mind[sit][idx] = max(1, mind[sit][idx] - 1)  # slight punishment

    print("Updated weights:", mind[sit])
    time.sleep(5)
