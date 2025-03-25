import random

chunk_seed = hash(f"{10},{20}")

print(f"Semilla: {chunk_seed}")

random.seed(chunk_seed)

# Guardar el estado inicial del generador
initial_state = random.getstate()

# Generar un número aleatorio
print("Número aleatorio 1:", random.randint(1, 100))

# Generar otro número aleatorio
print("Número aleatorio 2:", random.randint(1, 100))

# Restaurar el estado inicial
random.setstate(initial_state)

# Volver a generar un número aleatorio
# Este número será igual al primer número generado antes de guardar el estado
print("Número aleatorio 3 (igual al 1):", random.randint(1, 100))