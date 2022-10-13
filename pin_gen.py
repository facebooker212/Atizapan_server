import os
import random
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

print("ONLY RUN WITH ADMIN PERMISSION")

def resetPin():
    c = input("Are you sure you want to reset the PIN? (Y/N) ")
    if c == "Y":
        newKey = ""
        for i in range(0, 4):
            newKey += str(random.randint(0, 9))
        os.environ["PIN"] = newKey
        print(os.environ["PIN"])
        dotenv.set_key(dotenv_file, "PIN", os.environ["PIN"])
    elif c == "N":
        print("PIN not changed")
    else:
        print("Please use (Y/N)")
        resetPin()

resetPin()
