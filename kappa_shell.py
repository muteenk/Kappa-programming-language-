import kappa
from os import system, name 

print("=================Kappa================")
while True:
    try:
        inp = input("Kappa >> ")
    
        if inp == "--exit":
            break

        elif inp == "" or inp == "\t" or inp == " ":
            continue

        elif inp == "--clear":
            # for windows 
            if name == 'nt': 
                _ = system('cls') 
    
            # for mac and linux(here, os.name is 'posix') 
            else: 
                _ = system('clear') 

        else:
            print(kappa.exec(inp))

    except KeyboardInterrupt:
        print("keyboard interrupted:\n\tif u want to exit the kappa shell type => (--exit) keyword")