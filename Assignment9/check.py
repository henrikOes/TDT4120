# !/usr/bin/python3
# coding=utf-8

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# De lokale testene består av to deler. Et lite sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å teste på
# et større sett med 1000 genererte instanser. For å teste på det
# større settet med genererte instanser, må du (1) laste ned filen med
# testene fra øvingssystemet, (2) legge den samme plass som denne
# python-filen og (3) sette variabelen under til True.
use_extra_tests = False


def check(variables, constraints):
    # --- 1. Union-Find struktur ---
    parent = {v: v for v in variables}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[ry] = rx

    # --- 2. Samle opp likheter ---
    for a, comp, b in constraints:
        if comp == "=":
            union(a, b)

    # --- 3. Bygg graf for ulikheter mellom representanter ---
    from collections import defaultdict
    graph = defaultdict(set)
    indeg = defaultdict(int)

    for a, comp, b in constraints:
        ra, rb = find(a), find(b)
        if comp == "<":
            if ra == rb:  # konflikt: samme klasse kan ikke være < seg selv
                return False
            if rb not in graph[ra]:
                graph[ra].add(rb)
                indeg[rb] += 1
                indeg.setdefault(ra, 0)
        elif comp == ">":
            if ra == rb:
                return False
            if ra not in graph[rb]:
                graph[rb].add(ra)
                indeg[ra] += 1
                indeg.setdefault(rb, 0)

    # --- 4. Topologisk sort for å sjekke sykel ---
    from collections import deque
    queue = deque([n for n in indeg if indeg[n] == 0])
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for nb in graph[node]:
            indeg[nb] -= 1
            if indeg[nb] == 0:
                queue.append(nb)

    # Hvis vi ikke fikk besøkt alle noder => sykel
    if visited != len(indeg):
        return False

    return True


# Hardkodete tester på format: (variables, constraints), riktig svar
tests = [
    ((["x1"], []), True),
    ((["x1", "x2"], [("x1", "=", "x2")]), True),
    ((["x1"], [("x1", ">", "x1")]), False),
    ((["x1"], [("x1", "=", "x1")]), True),
    ((["x1", "x2"], [("x1", "<", "x2")]), True),
    ((["x1", "x2"], [("x2", "<", "x1"), ("x1", "=", "x2")]), False),
    ((["x1", "x2"], [("x2", ">", "x1"), ("x1", "<", "x2")]), True),
    ((["x1", "x2"], [("x1", ">", "x2"), ("x2", ">", "x1")]), False),
    (
        (
            ["x1", "x2", "x3"],
            [("x1", "<", "x2"), ("x2", "<", "x3"), ("x1", ">", "x3")],
        ),
        False,
    ),
    (
        (
            ["x1", "x2", "x3"],
            [("x1", "<", "x2"), ("x3", "=", "x1"), ("x2", "<", "x3")],
        ),
        False,
    ),
    ((["x4", "x0", "x1"], [("x1", "<", "x0")]), True),
    ((["x5", "x8"], [("x8", "<", "x5"), ("x8", "<", "x5")]), True),
    ((["x1", "x0", "x2"], []), True),
    (
        (
            ["x4", "x8", "x5"],
            [("x4", "<", "x5"), ("x8", ">", "x5"), ("x5", "<", "x8")],
        ),
        True,
    ),
    (
        (
            ["x5", "x9", "x0"],
            [
                ("x9", ">", "x5"),
                ("x9", "=", "x0"),
                ("x0", "=", "x9"),
                ("x0", "=", "x9"),
            ],
        ),
        True,
    ),
    (
        (
            ["x0", "x6", "x7"],
            [("x7", "=", "x0"), ("x7", ">", "x0"), ("x6", ">", "x0")],
        ),
        False,
    ),
    ((["x8", "x6", "x0"], []), True),
    (
        (
            ["x8", "x7", "x0"],
            [("x8", "=", "x0"), ("x0", "=", "x8"), ("x0", "=", "x8")],
        ),
        True,
    ),
    (
        (
            ["x8", "x4"],
            [
                ("x4", ">", "x8"),
                ("x4", ">", "x8"),
                ("x8", "<", "x4"),
                ("x4", ">", "x8"),
                ("x8", "=", "x4"),
            ],
        ),
        False,
    ),
    ((["x3", "x8", "x5"], [("x3", ">", "x8")]), True),
]


failed = False
for test_case, answer in tests:
    variables, constraints = test_case
    student = check(variables, constraints)
    if student != answer:
        if failed:
            print("-"*50)
        failed = True
        print(f"""
Koden feilet for følgende instans:
variables: {', '.join(variables)}
constraints:
    {(chr(10) + '    ').join(' '.join(x) for x in constraints)}

Ditt svar: {student}
Riktig svar: {answer}
""")

if use_extra_tests:
    with open("tests_theory_solver.txt") as extra_tests_data:
        extra_tests = []
        for line in extra_tests_data:
            variables, constraints, answer = line.strip().split(" | ")
            variables = variables.split(",")
            constraints = [x.split(" ") for x in constraints.split(",")]
            extra_tests.append(((variables, constraints), bool(int(answer))))

    n_failed = 0
    for test_case, answer in extra_tests:
        variables, constraints = test_case
        student = check(variables, constraints)
        if student != answer:
            n_failed += 1
            if failed and n_failed <= 5:
                print("-"*50)

            failed = True
            if n_failed <= 5:
                print(f"""
Koden feilet for følgende instans:
variables: {', '.join(variables)}
constraints:
    {(chr(10) + '    ').join(' '.join(x) for x in constraints)}

Ditt svar: {student}
Riktig svar: {answer}
""")
            elif n_failed == 6:
                print("Koden har feilet for mer enn 5 av de ekstra testene.")
                print("De resterende feilene vil ikke skrives ut.")

    if n_failed > 0:
        print(f"Koden feilet for {n_failed} av de ekstra testene.")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")