import kappa
print()
print("=================Kappa================")
while True:
    print()
    inp = input("Kappa >> ")
    print()
    if inp == "--exit":
        break

    else:
        print(kappa.exec(inp))
