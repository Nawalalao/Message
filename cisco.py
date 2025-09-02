entrer = input("Entrez votre sudoku ligne par ligne, (en separant les chiffres par des espaces): \n")

sudoku = [[int(num) for num in line] for line in entrer.split() if line]

les_neuf = [i for i in range(1, 10)]

first_step = True
second_step = True
third_step = True

step = [first_step, second_step, third_step]

for i in range(9):
    if sorted(sudoku[i]) != les_neuf:
        first_step = True
    else:
        first_step = False

for j in range(9):
    if sorted(sudoku[i][j] for i in range(9)) != les_neuf:
        print("colonne", j, "incorrecte")
        second_step = True
    else:
        second_step = False

for i in range(9):
    for j in range(9):
        if sorted(sudoku[3*(i//3) + k//3][3*(j//3)+k%3]for k in range(9)) != les_neuf:
            third_step = True
        else:
            third_step = False

if not (first_step or second_step or third_step):
    print("Sudoko correct")
else:
    print("Sudoku incorrect")
"""

295743861
431865927
876192543
387459216
612387495
549216738
763524189
928671354
154938672


"""