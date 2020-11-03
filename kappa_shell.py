import kappa

print("=================Kappa================")
while True:
    inp = input("Kappa >> ")
    
    if inp == "--exit":
        break

    else:
        print(kappa.exec(inp))