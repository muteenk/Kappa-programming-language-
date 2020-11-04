import kappa

print("=================Kappa================")
while True:
    inp = input("Kappa >> ")
    
    if inp == "--exit":
        break

    elif inp == "":
        continue

    else:
        print(kappa.exec(inp))