import tkinter as tk

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("INDICACIONES")
ventana.geometry("800x600")  # Establecer tamaño de la ventana

# Crear un marco para las indicaciones
frame = tk.Frame(ventana, padx=20, pady=20)
frame.pack(expand=True)

# Título de las indicaciones
titulo = tk.Label(frame, text="Instrucciones del Juego", font=("Arial", 24, "bold"))
titulo.pack(pady=10)

# Texto de las indicaciones
texto = """
1. Usa las teclas de movimiento (W, A, S, D o las flechas) para mover al personaje.
2. Presiona 'E' para interactuar con los árboles y piedras.
3. Presiona 'I' para abrir o cerrar el inventario.
4. Presiona 'F' para comer y recuperar hambre.
5. Presiona 'T' para beber y recuperar sed.
6. Evita que tu energía, hambre o sed lleguen a 0, o perderás el juego.
"""
indicaciones = tk.Label(frame, text=texto, font=("Arial", 14), justify="left", wraplength=750)
indicaciones.pack(pady=10)

# Botón para cerrar la ventana
boton_cerrar = tk.Button(frame, text="Cerrar", command=ventana.destroy, font=("Arial", 14))
boton_cerrar.pack(pady=20)

# Iniciar el bucle principal de la ventana
ventana.mainloop()