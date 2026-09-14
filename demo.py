"""Quick demo script for the GGM Agent System."""


def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to the GGM Agent System."


def add(a: float, b: float) -> float:
    return a + b


if __name__ == "__main__":
    print(greet("Jørgen"))
    print(f"2 + 3 = {add(2, 3)}")
