#!/usr/bin/python3
# coding=utf-8
import itertools
import random

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres.
random_tests = 10
# Laveste mulige antall rader og kolonner i generert instans.
n_lower = 3
# Høyest mulig antall rader og kolonner i generert instans.
# NB: Om dette antallet settes høyt vil det ta veldig lang tid å kjøre
# testene, da mulige svar sjekkes ved bruteforce.
n_upper = 5
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def shortest_road(build_map, start, end):
    from collections import deque
    
    if not build_map or not build_map[0]:
        return None
    
    rows, cols = len(build_map), len(build_map[0])
    
    # Check if start and end positions are valid and buildable
    if (start[0] < 0 or start[0] >= rows or start[1] < 0 or start[1] >= cols or
        end[0] < 0 or end[0] >= rows or end[1] < 0 or end[1] >= cols or
        not build_map[start[0]][start[1]] or not build_map[end[0]][end[1]]):
        return None
    
    # If start and end are the same
    if start == end:
        return [start]
    
    # BFS to find shortest path
    queue = deque([(start, [start])])  # (current_position, path_to_current)
    visited = set([start])
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        (current_row, current_col), path = queue.popleft()
        
        # Explore all 4 directions
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            new_pos = (new_row, new_col)
            
            # Check bounds and if position is buildable and not visited
            if (0 <= new_row < rows and 0 <= new_col < cols and
                build_map[new_row][new_col] and new_pos not in visited):
                
                new_path = path + [new_pos]
                
                # Check if we reached the end
                if new_pos == end:
                    return new_path
                
                # Add to queue for further exploration
                queue.append((new_pos, new_path))
                visited.add(new_pos)
    
    # No path found
    return None
    


# Disjoint-set forest
class Set:
    def __init__(self):
        self.__p = self
        self.rank = 0

    @property
    def p(self):
        if self.__p != self:
            self.__p = self.__p.p
        return self.__p

    @p.setter
    def p(self, value):
        self.__p = value.p


def union(x, y):
    x = x.p
    y = y.p
    if x.rank > y.rank:
        y.p = x
    else:
        x.p = y
        y.rank += x.rank == y.rank


# Hardkodete tester på format: (build_map, start, end), lengde på korteste vei
tests = [
    (([[True, True]], (0, 1), (0, 0)), 2),
    (([[True, False, True]], (0, 0), (0, 2)), None),
    (([[True, True, True]], (0, 0), (0, 2)), 3),
    (([[True, True, False]], (0, 1), (0, 0)), 2),
    (([[True], [True]], (1, 0), (0, 0)), 2),
    (([[True, False], [True, True]], (0, 0), (1, 1)), 3),
    (([[False, True], [True, True]], (0, 1), (1, 0)), 3),
    (([[True, True], [True, True]], (1, 1), (0, 0)), 3),
    (([[False, False, True], [True, False, True]], (1, 2), (0, 2)), 2),
    (([[False, False], [True, True], [False, False]], (1, 1), (1, 0)), 2),
    (([[True, False], [True, False]], (0, 0), (1, 0)), 2),
    (([[True, False], [False, False], [True, True]], (0, 0), (2, 1)), None),
    (([[False, False, True], [False, False, True], [True, False, True]], (0, 2), (2, 2)), 3),
    (([[False, False], [True, True], [False, False]], (1, 1), (1, 0)), 2),
    (([[True, True, True], [False, False, False]], (0, 2), (0, 1)), 2),
    (([[True, False, True], [True, False, False]], (0, 2), (1, 0)), None),
    (([[True, True], [False, False], [False, True]], (0, 0), (0, 1)), 2),
    (([[False, True, False], [False, True, False]], (1, 1), (0, 1)), 2),
]


# Treg bruteforce løsning
def bruteforce_solve(build_map, start, end):
    coordinates = set((x, y) for x in range(len(build_map))
                             for y in range(len(build_map[0]))
                             if build_map[x][y]
                      )
    coordinates -= {start, end}
    if verify_answer_internal(build_map, start, end, [start, end]) is None:
        return 2
    for k in range(1, len(coordinates) + 1):
        if any(verify_answer_internal(build_map, start, end,
                                      [start] + list(perm) + [end]) is None
               for perm in itertools.permutations(coordinates, r=k)):
            return k + 2
    return None


def verify_answer_internal(build_map, start, end, student):
    for pos in student:
        if not (
            0 <= pos[0] < len(build_map)
            and 0 <= pos[1] < len(build_map[0])
        ):
            return "Du prøver å bygge utenfor kartet."
        if not build_map[pos[0]][pos[1]]:
            return "Du prøver å bygge en plass der det ikke er mulig å bygge."
    else:
        disjoint_set = {pos: Set() for pos in student}
        for pos in student:
            for i, j in [
                (pos[0] + 1, pos[1]),
                (pos[0] - 1, pos[1]),
                (pos[0], pos[1] + 1),
                (pos[0], pos[1] - 1),
            ]:
                if (i, j) in disjoint_set and disjoint_set[
                    (i, j)
                ].p != disjoint_set[pos].p:
                    union(disjoint_set[pos], disjoint_set[(i, j)])
        if start not in disjoint_set:
            return "Du har ikke med startlandsbyen i listen."
        if end not in disjoint_set:
            return "Du har ikke med sluttlandsbyen i listen."
        if disjoint_set[start].p != disjoint_set[end].p:
            return "Listen din gir ikke en sammenhengende vei."


def verify_answer(build_map, start, end, student, answer):
    if answer is None and student is not None:
        return "Du returnerte en liste med posisjoner når riktig svar var None."
    if student is None and answer is not None:
        return "Du returnerte None, selv om det finnes en løsning."
    if student is not None and answer < len(student):
        return "Det finnes en liste med færre koordinater som fortsatt danner en gyldig vei."
    if student is not None:
        return verify_answer_internal(build_map, start, end, student)


def gen_examples(nl, nu, k):
    for _ in range(k):
        prob = random.randint(0, 10)/10
        rows = random.randint(min(nl, 2), nu)
        columns = random.randint(min(nl, 1), nu)
        start = (random.randint(0, rows - 1), random.randint(0, columns - 1))
        end = start
        while end == start:
            end = (random.randint(0, rows - 1), random.randint(0, columns - 1))
        build_map = [
            [random.random() < prob for _ in range(columns)]
            for _ in range(rows)
        ]
        build_map[start[0]][start[1]] = True
        build_map[end[0]][end[1]] = True
        yield (build_map, start, end), bruteforce_solve(build_map, start, end)


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(n_lower, n_upper, random_tests))

failed = False
for test_case, answer in tests:
    build_map, start, end = test_case
    student_map = [i[:] for i in build_map]
    student = shortest_road(student_map, start, end)
    response = verify_answer(build_map, start, end, student, answer)
    if response is not None:
        if failed:
            print("-"*50)
        failed = True
        map_string = "#" * (2 + len(build_map[0])) + "\n#" + \
                      "#\n#".join("".join([" ", "X"][not x] for x in row) for row in build_map) + \
                      "#\n" + "#" * (2 + len(build_map[0]))
        print(f"""
Koden feilet for følgende instans.
build_map: ({build_map})
{map_string}

start: {start}
end: {end}

Feilmelding: {response}
Ditt svar: {student}
        """)

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")
