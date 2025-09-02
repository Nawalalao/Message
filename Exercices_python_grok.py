digits = [ 
    '1111110',   # 0
    '0110000',   # 1
    '1101101',   # 2
    '1111001',   # 3
    '0110011',   # 4
    '1011011',   # 5
    '1011111',   # 6
    '1110000',   # 7
    '1111111',   # 8
    '1111011',   # 9
]

def render_digit(pattern):
    """Retourne les 5 lignes ASCII pour un chiffre"""
    a, b, c, d, e, f, g = [x == '1' for x in pattern]

    line1 = " _ " if a else "   "
    line2 = "{} {}".format("|" if f else " ", "|" if b else " ")
    line3 = " _ " if g else "   "
    line4 = "{} {}".format("|" if e else " ", "|" if c else " ")
    line5 = " _ " if d else "   "

    return [line1, line2, line3, line4, line5]


def display_number(num_str):
    """Affiche un nombre entier sur plusieurs digits 7 segments"""
    lines = ["", "", "", "", ""]

    for ch in num_str:
        digit = int(ch)
        pattern = digits[digit]
        rendered = render_digit(pattern)
        for i in range(5):
            lines[i] += rendered[i] + "  "  # espace entre chiffres

    for line in lines:
        print(line)


# Exemple : afficher "2025"
display_number("17")


# s = []
# s += list(map(int, input("Entrez des nombres séparés par des espaces: ").split()))
# print(sum(s))

"""
Exercices
Voici des exercices simples pour pratiquer.
 Essaie de les résoudre dans un interpréteur Python, puis vérifie tes réponses.

Comparaison de strings : Écris du code pour vérifier si 'Paris' < 'paris'. 
Explique pourquoi. (Indice : casse sensible.)
Tri de liste : Crée une liste fruits = ['pomme', 'banane', 'ananas']. 
Trie-la en ordre alphabétique croissant avec sorted(), puis en décroissant.
 Affiche les résultats.
String vs Number : Essaie de comparer '10' > 5. Ça marche ? 
Corrige pour que ça marche en convertissant. Que se passe-t-il si tu fais str(10) > '5' ?
Exercice mixte : Crée une liste mixte = ['2', '10', '3']. 
Convertis tous en entiers, puis trie-la numériquement. Résultat attendu : [2, 3, 10].
Tri avancé : Trie la liste mots = ['chat', 'chien', 'oiseau', 'poisson'] par longueur des mots (du plus court au plus long).
 Utilise key=len.

Résumé

"""
# mixte = ['2', '10', '3']

# # for i in mixte:
# #     mixte[mixte.index(i)] = int(i)
    

# # print(sorted(mixte))


# for i in mixte:
#     print(i)
    
# print(mixte)

text = input("Enter your message: ")
cipher = ''
for char in text:
    if not char.isalpha():
        continue
    char = char.upper()
    code = ord(char) + 1
    if code > ord('Z'):
        code = ord('A')
    cipher += chr(code)

print(cipher)

# Caesar cipher - decrypting a message.
cipher = input('Enter your cryptogram: ')
text = ''
for char in cipher:
    if not char.isalpha():
        continue
    char = char.upper()
    code = ord(char) - 1
    if code < ord('A'):
        code = ord('Z')
    text += chr(code)

print(text)
    


# sum of numbers

line = input("Enter a line of numbers - separate them with spaces: ")
strings = line.split()
total = 0
try:
    for substr in strings:
        total += float(substr)
    print("The total is:", total)
except:
    print(substr, "is not a number.")
    

