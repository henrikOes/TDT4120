import random

use_extra_tests = False

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


#("{count: 0, children: {'C': {count: 1, children: {}}}}", "CAA"), 0)
#(("{count: 1, children: {}}", "A"), 0),

class Node:
    def __init__(self):
        self.children = {}
        self.count = 0

    def __str__(self):
        representation = f"â”ƒ count: {self.count}\n"
        r = 0
        for symbol, node in self.children.items():
            r += 1
            if r == 1:
                representation += "â”ƒ\n"
            if r != 1:
                representation += "\n"
            if r != len(self.children):
                representation += f"â”£â”â”â”â”“ {symbol}"
                representation += "\nâ”ƒ   " + str(node).replace("\n", "\nâ”ƒ   ")
            else:
                representation += f"â”—â”â”â”â”“ {symbol}"
                representation += "\n    " + str(node).replace("\n", "\n    ")
        return representation

    @classmethod
    def from_string(cls, s):
        node = Node()
        ind = 0
        ind = s.index("count") + len("count: ")
        ind2 = s.index(",", ind)
        node.count = int(s[ind:ind2])
        ind = s.index("{", ind) + 1
        while ind != len(s) - 2:
            ind = s.index("'", ind) + 1
            c = s[ind]
            ind = s.index("{", ind)
            ind2 = ind + 1
            count = 1
            while count:
                if s[ind2] == "{":
                    count += 1
                if s[ind2] == "}":
                    count -= 1
                ind2 += 1
            node.children[c] = Node.from_string(s[ind:ind2])
            ind = ind2
        return node


tests = [
    (("{count: 1, children: {}}", ""), 1),
    (("{count: 0, children: {}}", ""), 0),
    (("{count: 1, children: {}}", "A"), 0),
    (("{count: 2000, children: {}}", ""), 2000),
    (("{count: 0, children: {'A': {count: 1, children: {}}}}", ""), 0),
    (("{count: 0, children: {'A': {count: 2, children: {}}}}", "A"), 2),
    (
        (
            "{count: 0, children: {'A': {count: 0, children: {'A': {count: 2, children: {}}}}}}",
            "A",
        ),
        0,
    ),
    (
        (
            "{count: 0, children: {'A': {count: 0, children: {'A': {count: 2, children: {}}}}}}",
            "B",
        ),
        0,
    ),
    (
        (
            "{count: 0, children: {'A': {count: 0, children: {'A': {count: 2, children: {}}}}}}",
            "AA",
        ),
        2,
    ),
    (("{count: 0, children: {}}", ""), 0),
    (
        (
            "{count: 1, children: {'T': {count: 0, children: {'G': {count: 0, children: {'C': {count: 1, children: {}}}}}}, 'A': {count: 0, children: {'C': {count: 1, children: {}}}}}}",
            "AC",
        ),
        1,
    ),
    (
        (
            "{count: 1, children: {'G': {count: 0, children: {'A': {count: 0, children: {'A': {count: 0, children: {'G': {count: 1, children: {}}}}}}}}}}",
            "",
        ),
        1,
    ),
    (("{count: 0, children: {}}", "GCAAC"), 0),
    (("{count: 0, children: {}}", "TGC"), 0),
    (
        (
            "{count: 0, children: {'T': {count: 0, children: {'T': {count: 0, children: {'C': {count: 0, children: {'A': {count: 1, children: {}}}}}}, 'G': {count: 1, children: {}}}}}}",
            "TCTCT",
        ),
        0,
    ),
    (
        (
            "{count: 0, children: {'A': {count: 0, children: {'C': {count: 0, children: {'C': {count: 0, children: {'T': {count: 0, children: {'A': {count: 1, children: {}}}}}}}}}}, 'T': {count: 0, children: {'C': {count: 2, children: {}}}}}}",
            "TGA",
        ),
        0,
    ),
    (("{count: 0, children: {}}", ""), 0),
    (
        (
            "{count: 0, children: {'T': {count: 0, children: {'C': {count: 0, children: {'T': {count: 0, children: {'C': {count: 1, children: {}}}}}}}}, 'G': {count: 1, children: {}}}}",
            "TCTC",
        ),
        1,
    ),
    (("{count: 0, children: {'C': {count: 1, children: {}}}}", "CAA"), 0),
]


failed = False
for test_case, answer in tests:
    root, dna = test_case
    root = Node.from_string(root)
    student = search_tree(root, dna)
    if student != answer:
        if failed:
            print("-"*50)

        failed = True
        print(f"""
Koden feilet for fÃ¸lgende instans:
dna: {dna if dna else "(tom streng)"}
tree:
{root}

Ditt svar: {student}
Riktig svar: {answer}
        """)

if use_extra_tests:
    with open("tests_search_tree.txt") as extra_tests_data:
        extra_tests = []
        for line in extra_tests_data:
            tree, dna, answer = line.strip().split(" | ")
            root = Node.from_string(tree)
            answer = int(answer)
            extra_tests.append((
                (root, dna),
                answer,
            ))

    n_failed = 0
    for test_case, answer in extra_tests:
        root, dna = test_case
        student = search_tree(root, dna)
        if student != answer:
            n_failed += 1
            if failed and n_failed <= 5:
                print("-"*50)

            failed = True
            if n_failed <= 5:
                print(f"""
Koden feilet for fÃ¸lgende instans:
dna: {dna if dna else "(tom streng)"}
tree:
{root}

Ditt svar: {student}
Riktig svar: {answer}
                """)
            elif n_failed == 6:
                print("Koden har feilet for mer enn 5 av de ekstra testene.")
                print("De resterende feilene vil ikke skrives ut.")

    if n_failed > 0:
        print(f"Koden feilet for {n_failed} av de ekstra testene.")



if not failed:
    print("Koden din fungerte for alle eksempeltestene")