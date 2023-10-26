import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import csv
from tkinter import messagebox
import re

class Habitacion:
    def __init__(self, numero, tipo, costo):
        self.numero = numero
        self.tipo = tipo
        self.costo = costo

class HabitacionSencilla(Habitacion):
    def __init__(self, numero):
        super().__init__(numero, "Sencilla", costo=100)

class HabitacionDoble(Habitacion):
    def __init__(self, numero):
        super().__init__(numero, "Doble", costo=150)

class HabitacionSuite(Habitacion):
    def __init__(self, numero):
        super().__init__(numero, "Suite", costo=200)

class Reserva:
    def __init__(self, habitacion, huesped, ingreso, salida, telefono):
        self.habitacion = habitacion
        self.huesped = huesped
        self.ingreso = ingreso
        self.salida = salida
        self.telefono = telefono

    def calcular_costo(self):
        # Calcula el costo total de la reserva basado en las fechas y el costo de la habitación
        dias = (self.salida - self.ingreso).days
        return self.habitacion.costo * dias

class Huesped:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

# Precargar habitaciones
habitaciones_precargadas = [HabitacionSencilla(i) for i in range(1, 4)]
habitaciones_precargadas += [HabitacionDoble(i) for i in range(4, 7)]
habitaciones_precargadas += [HabitacionSuite(i) for i in range(7, 10)]

def guardar_reservas(reservas):
    with open("reservas.csv", mode="w", newline="") as file:
        reserva_writer = csv.writer(file)
        for reserva in reservas:
            reserva_writer.writerow([reserva.huesped.nombre, reserva.huesped.email, reserva.habitacion.numero, reserva.habitacion.tipo, reserva.ingreso, reserva.salida, reserva.telefono])

# Crear y cargar las reservas desde el archivo CSV
reservas = []

def cargar_reservas():
    reservas = []
    try:
        with open("reservas.csv", mode="r") as file:
            reserva_reader = csv.reader(file)
            for row in reserva_reader:
                nombre, email, numero_habitacion, tipo_habitacion, ingreso, salida, telefono = row
                habitacion = None
                for habit in habitaciones_precargadas:
                    if habit.tipo == tipo_habitacion:
                        habitacion = habit
                        break
                huesped = Huesped(nombre, email)
                reserva = Reserva(habitacion, huesped, ingreso, salida, telefono)
                reservas.append(reserva)
    except FileNotFoundError:
        pass
    return reservas

reservas = cargar_reservas()

def habitacion_disponible(habitacion, ingreso, salida):
    for reserva in reservas:
        if reserva.habitacion == habitacion:
            if (ingreso < reserva.salida) and (salida > reserva.ingreso):
                return False
    return True

def hacer_reserva():
    nombre = nombre_entry.get()
    email = email_entry.get()
    habitacion = tipo_combobox.get()
    ingreso = ingreso_cal.get_date()
    salida = salida_cal.get_date()
    telefono = telefono_entry.get()

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        tk.messagebox.showerror("Error", "Ingrese una dirección de correo electrónico válida.")
        return

    if not re.match(r"^\d{10}$", telefono):
        tk.messagebox.showerror("Error", "Ingrese un número de teléfono válido de 10 dígitos.")
        return

    for habitacion_precargada in habitaciones_precargadas:
        if habitacion_precargada.tipo == habitacion:
            break
    else:
        tk.messagebox.showerror("Error", "Seleccione un tipo de habitación válido.")
        return
    if not habitacion_disponible(habitacion_precargada, ingreso, salida):
        tk.messagebox.showerror("Error", "La habitación no está disponible en las fechas seleccionadas.")
        return

    new_reserva = Reserva(habitacion_precargada, Huesped(nombre, email), ingreso, salida, telefono)
    reservas.append(new_reserva)
    guardar_reservas(reservas)

    nombre_entry.delete(0, "end")
    email_entry.delete(0, "end")
    tipo_combobox.set("Sencilla")
    ingreso_cal.set_date("")
    salida_cal.set_date("")
    telefono_entry.delete(0, "end")

def mostrar_reservas():
    resultado_text.delete(1.0, "end")  # Borra todo el contenido actual

    for reserva in reservas:
        costo = reserva.calcular_costo()
        resultado_text.insert("end", f"{reserva.huesped.nombre} ({reserva.huesped.email}) - Habitación {reserva.habitacion.numero} ({reserva.habitacion.tipo}) - Ingreso: {reserva.ingreso} - Salida: {reserva.salida} - Costo: ${costo} - Teléfono: {reserva.telefono}\n")

root = tk.Tk()
root.title("Hotel Reservations")

nombre_label = tk.Label(root, text="Nombre del huésped:")
nombre_label.pack()
nombre_entry = tk.Entry(root)
nombre_entry.pack()

email_label = tk.Label(root, text="Correo electrónico:")
email_label.pack()
email_entry = tk.Entry(root)
email_entry.pack()

tipo_label = tk.Label(root, text="Tipo de habitación:")
tipo_label.pack()
tipos_habitacion = ["Sencilla", "Doble", "Suite"]
tipo_combobox = ttk.Combobox(root, values=tipos_habitacion)
tipo_combobox.set("Sencilla")
tipo_combobox.pack()

ingreso_label = tk.Label(root, text="Fecha de ingreso:")
ingreso_label.pack()
ingreso_cal = DateEntry(root, width=12)
ingreso_cal.pack()

salida_label = tk.Label(root, text="Fecha de salida:")
salida_label.pack()
salida_cal = DateEntry(root, width=12)
salida_cal.pack()

telefono_label = tk.Label(root, text="Número de teléfono:")
telefono_label.pack()
telefono_entry = tk.Entry(root)
telefono_entry.pack()

reservar_button = tk.Button(root, text="Hacer Reserva", command=hacer_reserva)
reservar_button.pack()

mostrar_button = tk.Button(root, text="Mostrar Reservas", command=mostrar_reservas)
mostrar_button.pack()

resultado_text = tk.Text(root, width=40, height=10)
resultado_text.pack()

root.mainloop()
