# !/usr/bin/python3
# coding=utf-8
import sys
sys.set_int_max_str_digits(10**6)

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# De lokale testene består av to deler. Et lite sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å teste på
# et større sett med 500 genererte instanser. For å teste på det
# større settet med genererte instanser, må du (1) laste ned filen med
# testene fra øvingssystemet, (2) legge den samme plass som denne
# python-filen og (3) sette variabelen under til True. Merk at det kan
# ta litt tid å kjøre alle de 500 ekstra testene.
use_extra_tests = False

def schulze_method(W, n):
    # Use the local implementation of Floyd--Warshall instead of importing.
    class Operator:
        def __init__(self, name, function):
            self.name = name
            self.function = function

    def general_floyd_warshall(D, n, f, g):
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    D[i][j] = f(D[i][j], g(D[i][k], D[k][j]))
    # No external imports allowed here

    f = Operator("maximum", lambda x, y: max(x, y))
    g = Operator("minimum", lambda x, y: min(x, y))

    general_floyd_warshall(W, n, f.function, g.function)

    # Sort by pairwise comparison using the computed strongest-path strengths.
    # Candidate a is ranked before b iff W[a][b] > W[b][a].
    def compare(a, b):
        if W[a][b] > W[b][a]:
            return -1
        if W[a][b] < W[b][a]:
            return 1
        # tie-break deterministically by candidate index
        return a - b

    # Sort indices using a simple insertion sort and the compare function.
    ranking = list(range(n))
    for i in range(1, n):
        key = ranking[i]
        j = i - 1
        # move elements that should come after 'key' one position ahead
        while j >= 0 and compare(key, ranking[j]) < 0:
            ranking[j + 1] = ranking[j]
            j -= 1
        ranking[j + 1] = key
    return ranking


# Hardkodete tester på format: (W, svar)
tests = [
    ([[0]], [0]),
    ([[0, 1], [3, 0]], [1, 0]),
    ([[0, 2], [2, 0]], [0, 1]),
    ([[0, 4, 3], [2, 0, 2], [3, 4, 0]], [0, 2, 1]),
    ([[0, 2, 1], [4, 0, 4], [5, 2, 0]], [1, 2, 0]),
    (
        [
            [0, 1, 3, 3, 3],
            [9, 0, 5, 5, 7],
            [7, 5, 0, 5, 4],
            [7, 5, 5, 0, 6],
            [7, 3, 6, 4, 0],
        ],
        [1, 3, 4, 2, 0],
    ),
    (
        [
            [0, 6, 7, 8, 7, 8],
            [6, 0, 6, 8, 7, 8],
            [5, 6, 0, 6, 5, 7],
            [4, 4, 6, 0, 5, 6],
            [5, 5, 7, 7, 0, 6],
            [4, 4, 5, 6, 6, 0],
        ],
        [0, 1, 4, 2, 3, 5],
    ),
]


def validate(student, answer):
    try:
        len(student)
    except:
        return "Koden returnerte ikke en liste"

    if len(student) != len(answer):
        return "Listen inneholder ikke riktig antall kandidater"

    if set(student) != set(answer):
        return "Listen inneholder ikke alle kandidatene"

    if any(a != b for a, b in zip(student, answer)):
        return "En eller flere av kandidatene opptrer i feil rekkefølge"


def generate_feedback(test, expected, student):
    feedback = ""
    feedback += "Koden din feilet for input\n"
    feedback += str(test) + "\n"
    feedback += "Ditt svar er\n"
    feedback += str(student) + ",\n"
    feedback += "men riktig svar er\n"
    feedback += str(expected) + "."
    return feedback


table_format = lambda T: "\n    " + "\n    ".join(map(str, T))
failed = False
for W, answer in tests:
    student = schulze_method([row[:] for row in W], len(W))
    feedback = validate(student, answer)
    if feedback is not None:
        if failed:
            print("-"*50)
        failed = True
        print(f"""
Koden feilet for følgende instans.
W: {table_format(W)}
n: {len(W)}

Ditt svar: {student}
Riktig svar: {answer}
Feedback: {feedback}
""")

if use_extra_tests:
    with open("tests_schulze_method.txt") as extra_tests_data:
        extra_tests = []
        for line in extra_tests_data:
            W, answer = map(eval, line.strip().split(" | "))
            extra_tests.append((W, answer))

    n_failed = 0
    for W, answer in extra_tests:
        student = schulze_method([row[:] for row in W], len(W))
        feedback = validate(student, answer)
        if feedback is not None:
            n_failed += 1
            if failed and n_failed <= 5:
                print("-"*50)

            failed = True
            if n_failed <= 5:
                print(f"""
Koden feilet for følgende instans.
W: {table_format(W)}
n: {len(W)}

Ditt svar: {student}
Riktig svar: {answer}
Feedback: {feedback}
""")
            elif n_failed == 6:
                print("Koden har feilet for mer enn 5 av de ekstra testene.")
                print("De resterende feilene vil ikke skrives ut.")

    if n_failed > 0:
        print(f"Koden feilet for {n_failed} av de ekstra testene.")

if not failed:
    print("Koden din passerte alle eksempeltestene.")