if __name__ == "__main__":
    with open("config.txt") as file:
        lines = sum(1 for line in file)
        print("Total number of lines:", lines)
# Security Width
    with open("config.txt") as vtf:
        line = vtf.readline(6)
        if (line == "WIDTH="):
            try:
                test = int(vtf.readline())
                print(test)
            except Exception as e:
                print(e)
# Security Height
        line = vtf.readline(7)
        if (line == "HEIGHT="):
            try:
                test = int(vtf.readline())
                print(test)
            except Exception as e:
                print(e)
# Security Entry
        line = vtf.readline(6)
        if line == "ENTRY=":
            fleuri = vtf.readline().split(',')
            coord: list[int] = []
            try:
                for i in range(len(fleuri)):
                    try:
                        coord = coord + [int(fleuri[i])]
                    except ValueError as ve:
                        print(ve)
                coords = (coord[0], coord[1])
            except Exception as ex:
                print(ex)
            else:
                print(coords)
# Security Exit
        line = vtf.readline(5)
        if line == "EXIT=":
            feneant = vtf.readline().split(',')
            cord: list[int] = []
            try:
                for i in range(len(feneant)):
                    try:
                        cord = cord + [int(feneant[i])]
                    except ValueError as ve:
                        print(ve)
                cords = (cord[0], cord[1])
            except Exception as ex:
                print(ex)
            else:
                print(cords)
# Security Output_File
        line = vtf.readline(12)
        if (line == "OUTPUT_FILE="):
            stout = vtf.readline().strip()
            print(stout)
# security Perfect
        line = vtf.readline(8)
        if (line == "PERFECT="):
            oemaiseh = False
            trueorfalse = vtf.readline()
            if (trueorfalse == "True"):
                oemaiseh = True
            if oemaiseh is True:
                print(oemaiseh)
