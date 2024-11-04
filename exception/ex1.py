def divEntier(x: int, y: int) -> int:
    if x < y:
        return 0
    else:
        x = x - y
        return divEntier(x, y) + 1


if __name__ == '__main__':
    try :
        x = int(input("Entrez une valeur de X :"))
        y = int(input("Entrez une valeur de Y :"))
        print(divEntier(x,y))
    except :
        print("Veuillez rentrer une valeur numérique")
