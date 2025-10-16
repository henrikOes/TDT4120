#!/usr/bin/python3
# coding=utf-8
import random
import string

# Testsettet på serveren er større og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke når du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt høyde for.

# De lokale testene består av to deler. Et sett med hardkodete instanser og
# muligheten for å generere tilfeldige instanser. Genereringen av de tilfeldige
# instansene kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres.
random_tests = 10
# Laveste mulige antall pakker i generert instans.
n_lower = 3
# Høyest mulig antall pakker i generert instans.
n_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def resolve_and_install(package):
    


class Package:
    def __init__(self, dependencies, is_installed_func):
        self.__is_installed_func = is_installed_func
        self.__dependencies = dependencies

    @property
    def dependencies(self):
        return self.__dependencies

    @property
    def is_installed(self):
        return self.__is_installed_func(self)

    def __str__(self):
        if not self.dependencies:
            return f"● is_installed: {self.is_installed}\n"
        representation = f"┓ is_installed: {self.is_installed}\n"
        r = 0
        for dependency in self.dependencies:
            r += 1
            if r != 1:
                representation += "\n"
            if r != len(self.dependencies):
                representation += f"┣━━━" + str(dependency).replace("\n", "\n┃   ")
            else:
                representation += f"┗━━━" + str(dependency).replace("\n", "\n    ")
        return representation

    def __repr__(self):
        return str(self)

    def deepcopy(self):
        def gen_function(val):
            return lambda x: val

        return Package(
            [dep.deepcopy() for dep in self.dependencies],
            gen_function(self.is_installed),
        )


def get_install_func(installed_packages):
    def install(package):
        if package.is_installed:
            raise ValueError(
                'Du kjører "install" på en pakke som allerede er installert.'
            )
        if not all([p.is_installed for p in package.dependencies]):
            raise ValueError(
                'Du kjører "install" på en pakke uten å ha installert alle pakkene den er avhengig av.'
            )
        installed_packages.add(package)

    return install


def generate_random_test(num_nodes, p):
    installed_packages = set()
    is_installed_func = lambda x: x in installed_packages
    packages = [None for i in range(num_nodes)]
    incoming_edges = [[] for i in range(num_nodes)]
    installed_limit = random.randint(0, num_nodes)
    for i in range(1, num_nodes):
        predecessors = random.sample(
            range(0, i), k=random.randint(1, min(i, max(1, int(2 * p * i))))
        )
        for pre in predecessors:
            incoming_edges[pre].append(i)
    for i in range(num_nodes - 1, -1, -1):
        dependencies = tuple([packages[j] for j in incoming_edges[i]])
        packages[i] = Package(dependencies, is_installed_func)
        if i >= installed_limit:
            installed_packages.add(packages[i])
    return (packages[0], get_install_func(installed_packages))

def gen_examples(nl, nu, k):
    for _ in range(k):
        yield generate_random_test(
                random.randint(nl, nu),
                random.randint(1, 9)/10
            )

random.seed(1)
tests = [
    generate_random_test(random.randint(1, 10), random.randint(4, 6)/10)
    for _ in range(10)
]

if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(n_lower, n_upper, random_tests))


failed = False
for package, install_func in tests:
    global install
    install = install_func
    initial_state = package.deepcopy()
    try:
        resolve_and_install(package)
    except ValueError as e:
        if failed:
            print("-"*50)
        print(f"""
Koden feilet med følgende feilmelding:
{str(e)}

Input:
{str(initial_state)}

Status ved avslutning:
{str(package)}
        """)
        failed = True
    else:
        if not package.is_installed:
            if failed:
                print("-"*50)
            print(f"""
Koden installerte ikke pakken.

Input:
{str(initial_state)}

Status ved avslutning:
{str(package)}
            """)
            failed = True

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")
