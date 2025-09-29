# !/usr/bin/python3
# coding=utf-8
import random

# Testsettet pÃ¥ serveren er stÃ¸rre og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke nÃ¥r du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt hÃ¸yde for.

# De lokale testene bestÃ¥r av to deler. Et sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for Ã¥ generere
# tilfeldig instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved Ã¥ juste pÃ¥ verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres
random_tests = 10
# Lavest mulig antall tegn i dna.
n_lower = 3
# HÃ¸yest mulig antall tegn i dna.
n_upper = 100
# Lavest mulig antall tegn i hvert segment.
d_lower = 1
# HÃ¸yest mulig antall tegn i hvert segment.
d_upper = 10
# Lavest mulig antall segmenter.
k_lower = 1
# HÃ¸yest mulig antall segmenter.
k_upper = 20
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def string_match(dna, segments):
    count = 0
    n = len(dna) #antall ord
    for segment in segments:
        d = len(segment) #lengden på segmentet
        # Gå gjennom alle substrenger av dna som har lengde lik segmentet
        for i in range(n - d + 1):
            if dna[i:i+d] == segment:
                count += 1
    return count

        
def search_tree(root, dna):
    # root er roten i treet og dna er strengen vi skal søke etter
    current_node = root
    if dna == "":
        return current_node.count
    
    for char in dna:
        if char in current_node.children:
            current_node = current_node.children[char]
        else:
            return 0  # stopper hvis path ikke finnes
    
    return current_node.count
        
def build_tree(dna_sequences):
    #Node() lager et tomt node objekt
    tree = Node()
    #Går gjennom alle dna sekvensene i listen
    for dna in dna_sequences:
        current_node = tree
        #Hvis dna sekvensen er tom, øker vi count på roten
        if dna == "":
            current_node.count += 1
            continue
        #Går gjennom alle bokstavene i dna sekvensen
        for char in dna:
            #Hvis bokstaven ikke er et barn av current_node, lager vi en ny node for bokstaven
            if char not in current_node.children:
                current_node.children[char] = Node()
            #Går ned til barnet som tilsvarer bokstaven
            current_node = current_node.children[char]
        #Når vi har gått gjennom hele dna sekvensen, øker vi count på den siste noden
        current_node.count += 1
    return tree

class Node:
    def __init__(self):
        self.children = {}
        self.count = 0

    def __str__(self):
        return (
            f"{{count: {self.count}, children: {{"
            + ", ".join(
                [f"'{c}': {node}" for c, node in self.children.items()]
            )
            + "}"
        )




# Hardkodete tester pÃ¥ format: ((dna, segments), riktig svar)
tests = [
    (("A", []), 0),
    (("AAAA", ["A"]), 4),
    (("ACTTACTGG", ["A", "ACT", "GG"]), 5),
    (("AAAAAAAAAAAAAAAAAAAA", ["A"]), 20),
    (("AAAAAAAAAAAAAAAAAAAA", ["AA"]), 19),
    (("AAAAAAAAAAAAAAAAAAAA", ["A", "A"]), 40),
    (("AAAAAAAAAAAAAAAAAAAA", ["A", "AA"]), 39),
    (("ABABABABABABABABABAB", ["AB"]), 10),
    (("ABABABABABABABABABAB", ["A", "AB"]), 20),
    (("ABABABABABABABABABAB", ["A", "B"]), 20),
]


# LÃ¸ser problemet ved bruteforce. Har kjÃ¸retid Î©(kn).
def bruteforce_solve(dna, segments):
    counter = 0
    for segment in segments:
        for i in range(len(dna) - len(segment) + 1):
            if dna[i : i + len(segment)] == segment:
                counter += 1
    return counter


def gen_examples(k, nl, nu, dl, du, kl, ku):
    for _ in range(k):
        n = random.randint(nl, nu)
        k_ = random.randint(kl, ku)
        dna = "".join(random.choices("AGTC", k=n))
        segments = [
            "".join(random.choices("AGTC", k=random.randint(dl, du)))
            for _ in range(k_)
        ]
        yield (dna, segments), bruteforce_solve(dna, segments)


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(
        random_tests,
        n_lower,
        n_upper,
        d_lower,
        d_upper,
        k_lower,
        k_upper,
    ))

failed = False

for test_case, answer in tests:
    dna, segments = test_case
    student_answer = string_match(dna, segments[:])
    if student_answer != answer:
        if failed:
            print("-"*50)
        failed = True

        print(f"""
Koden feilet for fÃ¸lgende instans:
dna: {dna}
segments: {", ".join(segments)}

Ditt svar: {student_answer}
Riktig svar: {answer}
""")

if not failed:
    print("Koden din fungerte for alle eksempeltestene")