# !/usr/bin/python3
# coding=utf-8
import random
import math

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres
random_tests = 10
# Lavest mulig antall tegn i dna.
n_lower = 3
# HÃ¸yest mulig antall tegn i dna.
# NB: Generering av instanser tar lang tid om denne verdien settes hÃ¸yt (>500)
n_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def longest_repeated_substring(dna, k):
    #dna er strengen vi skal finne substrenger i, k er antall ganger substringen må forekomme
    n = len(dna)
    longest_substring = None
    
    for length in range(n-1, 0, -1):
        substrings = {}
        for i in range(n - length + 1):
            substring = dna[i:i + length]
            if substring in substrings:
                substrings[substring] += 1
            else:
                substrings[substring] = 1
        
        found = False
        for substring, count in substrings.items():
            if count >= k:
                if longest_substring is None or len(substring) > len(longest_substring):
                    longest_substring = substring
                    found = True
        if found:
            break
        
    return longest_substring


# Hardkodete tester pÃ¥ formatet: ((dna, k), mulige svar)
tests = [
    (("A", 2), [None]),
    (("AA", 2), ["A"]),
    (("AA", 3), [None]),
    (("CAACAAC", 2), ["CAAC"]),
    (("CAACAAC", 3), ["A", "C"]),
    (("ACGTTGCA", 2), ["A", "C", "G", "T"]),
    (("ACGTTGCA", 3), [None]),
    (("ACTACTAGC", 2), ["ACTA"]),
    (("ACTACTAGC", 3), ["A", "C"]),
    (("ACTACTAGC", 4), [None]),
    (("ACTGTGTACGTGATAGCATA", 2), ["GTG", "ATA", "TGT"]),
    (("ACTGTGTACGTGATAGCATA", 3), ["TG", "TA", "GT"]),
    (("ACTGTGTACGTGATAGCATA", 4), ["A", "T", "G"]),
    (("ACTGTGTACGTGATAGCATA", 5), ["A", "T", "G"]),
    (("ACTGTGTACGTGATAGCATA", 6), ["A", "T"]),
    (("ACTGTGTACGTGATAGCATA", 7), [None]),
    (("ACGTGTGTGGCAGGCAGGTTGGAGGA", 2), ["GGCAGG"]),
    (("ACGTGTGTGGCAGGCAGGTTGGAGGA", 3), ["AGG", "GTG"]),
    (("ACGTGTGTGGCAGGCAGGTTGGAGGA", 4), ["GG", "GT", "TG"]),
    (("ACGTGTGTGGCAGGCAGGTTGGAGGA", 5), ["GG"]),
    (("ACGTGTGTGGCAGGCAGGTTGGAGGA", 6), ["G"]),
    (("ACGTGTGTGGCAGGCAGGTTGGAGGA", 7), ["G"]),
    (("ACGTGTGTGGCAGGCAGGTTGGAGGA", 8), ["G"]),
    (("ACGTGTGTGGCAGGCAGGTTGGAGGA", 9), ["G"]),
    (("ACGTGTGTGGCAGGCAGGTTGGAGGA", 10), ["G"]),
    (("ACGTGTGTGGCAGGCAGGTTGGAGGA", 15), [None]),
    (("AAAAAAAACAAAAAAAAC", 2), ["AAAAAAAAC"]),
    (("AAAAAAAACAAAAAAAAC", 3), ["AAAAAAA"]),
    (("AAAAAAAACAAAAAAAAC", 4), ["AAAAAAA"]),
    (("AAAAAAAACAAAAAAAAC", 5), ["AAAAAA"]),
    (("AAAAAAAACAAAAAAAAC", 6), ["AAAAAA"]),
    (("AAAAAAAACAAAAAAAAC", 7), ["AAAAA"]),
    (("AAAAAAAACAAAAAAAAC", 8), ["AAAAA"]),
    (("AAAAAAAACAAAAAAAAC", 10), ["AAAA"]),
    (("AAAAAAAACAAAAAAAAC", 16), ["A"]),
    (("AAAAAAAACAAAAAAAAC", 17), [None]),
]


# Bruteforce lÃ¸sning som finner alle gyldige lÃ¸sninger pÃ¥ problemet ved Ã¥ teste hver av disse
# individuelt. Har kjÃ¸retid Î©(n^3) og vil bruke veldig lang tid for store
# instanser.
def bruteforce_solve_all(dna, k):
    solutions = [None]
    for z in range(1, len(dna)):
        for i in range(len(dna)):
            sub = dna[i:i + z]
            count = 1
            for j in range(i + 1, len(dna)):
                if sub == dna[j:j + z]:
                    count += 1
            if count >= k:
                if solutions[0] is None or len(solutions[0]) < len(sub):
                    solutions = []
                solutions.append(sub)
    return solutions


def gen_examples(k, nl, nu):
    for _ in range(k):
        n = random.randint(nl, nu)
        dna = "".join(random.choices("ACGT", k=n))
        r = random.randint(2, math.ceil(math.log(n, 3) + 4))
        yield (dna, r), bruteforce_solve_all(dna, r)


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(random_tests, n_lower, n_upper))


failed = False

for test_case, possible_answers in tests:
    dna, k = test_case
    student_answer = longest_repeated_substring(dna, k)
    if student_answer not in possible_answers:
        if failed:
            print("-"*50)
        failed = True

        print(f"""
Koden feilet for fÃ¸lgende instans:
dna: {dna}
k: {k}

Ditt svar: {student_answer}
Riktig{"e" if len(possible_answers) > 1 else ""} svar: {", ".join(possible_answers)}
""")

if not failed:
    print("Koden din fungerte for alle eksempeltestene")