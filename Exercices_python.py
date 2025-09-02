etudiants = {
    "Clara": 12,
    "Alice": 15,
    "Bob": 18,
    "David": 9,
    "Eva": 15
}

noms = list(etudiants.keys())
notes = list(etudiants.values())

note_min = min(notes)
note_max = max(notes)

# dictionnaire pour stocker les notes normalisées
etudiants_normalisee = {}

for n, note in zip(noms, notes):
    etudiants_normalisee[n] = round((note - note_min) / (note_max - note_min), 2)

# affichage
for nom, note_norm in etudiants_normalisee.items():
    print(f"{nom} a obtenu une note normalisée de {note_norm}")


print("---"*15)
etudiants_normalisee_classer = sorted(etudiants_normalisee.items(), key=lambda x: x[1], reverse=True)

note_precedente = None

for rang, (nom, note) in enumerate(etudiants_normalisee_classer, start=1):    
    if note == note_precedente:
        # si la note est la meme que la precedente, on garde le meme rang
        print(f"{nom}a obtenu une note de {note} et est classer {rang - 1}")
    else:
        print(f"{nom} a obtenu une note de {note} et est classer {rang}")
        note_precedente = note
  