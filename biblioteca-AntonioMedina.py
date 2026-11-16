# variables globales 

Usuarios=[]

usuario={
    "nombre":"",
    "identificacion":"",
    "edad":0
}

Libros=[]

libro={
    "titulo": "titulo",
    "autor": "autor",
    "cantidad": 0,
    "disponibles": 0
}

Prestamos=[]



multa_por_dia= 2000 #pesos colombianos
dias_prestamo= 7 #dias del prestamo

#Registro de usuarios
def registrar_usuario():
    try:

        print("Registro de usuario")
        nombre=input("Ingrese el nombre del usuario: ")
        identificacion=input("Ingrese la identificación del usuario: ")
        edad=int(input("Ingrese la edad del usuario: "))

        while edad <= 0 or edad > 120:
            print("Error: Por favor, ingrese una edad válida.")

            edad=int(input("Ingrese la edad del usuario: "))

        usuario={
            "nombre":nombre,
            "identificacion":identificacion,
            "edad":edad
        }

        Usuarios.append(usuario)
        print("Usuario registrado exitosamente.")

    except ValueError:
        print("Error: Por favor, ingrese una edad válida.")
    except Exception as e:
        print(f"Error: {e}")

#Registro de Libros
def registrar_libro():
    try:
        print("Registro de libro")
        titulo=input("Ingrese el título del libro: ")
        autor=input("Ingrese el autor del libro: ")
        cantidad=int(input("Ingrese la cantidad de ejemplares: "))
        
        libro={
            "titulo":titulo,
            "autor":autor,
            "cantidad":cantidad,
            "disponibles":cantidad
        }

        Libros.append(libro)
        print("Libro registrado exitosamente.")

    except ValueError:
        print("Error: Por favor, ingrese una cantidad válida.")
    except Exception as e:
        print(f"Error: {e}")

#Consulta de Libros

def consultar_libros():
    if not Libros:
        print("No hay libros registrados.")
        return

    print("Libros disponibles:")
    for libro in Libros:
        print(f"Título: {libro['titulo']}, \n Autor: {libro['autor']}, \n Cantidad: {libro['cantidad']}, \n Disponibles: {libro['disponibles']}")

#Prestar Libro
def prestar_libro():
    try:
        if not Usuarios:
            print("No hay usuarios registrados. Por favor, registre un usuario primero.")
            return

        if not Libros:
            print("No hay libros registrados. Por favor, registre un libro primero.")
            return

        identificacion=input("Ingrese la identificación del usuario: ")
        usuario_encontrado = next((u for u in Usuarios if u["identificacion"] == identificacion), None)

        if not usuario_encontrado:
            print("Usuario no encontrado. Por favor, intente nuevamente.")
            return

        titulo=input("Ingrese el título del libro a prestar: ")
        libro_encontrado = next((l for l in Libros if l["titulo"] == titulo), None)

        if not libro_encontrado:
            print("Libro no encontrado. Por favor, registre el libro primero.")
            return

        if libro_encontrado["disponibles"] == 0:
            print("No hay ejemplares disponibles para este libro.")
            return

        from datetime import datetime, timedelta
        fecha_prestamo = datetime.now()
        fecha_limite = fecha_prestamo + timedelta(days=dias_prestamo)

        prestamo={
            "id": len(Prestamos) + 1,
            "usuario": identificacion,
            "libro": titulo,
            "fecha_prestamo": fecha_prestamo.strftime("%d/%m/%Y"),
            "fecha_limite": fecha_limite.strftime("%d/%m/%Y"),
            "devuelto": False
        }

        Prestamos.append(prestamo)
        libro_encontrado["disponibles"] -= 1
        print(f"Libro prestado exitosamente. Fecha límite de devolución: {fecha_limite.strftime('%d/%m/%Y')}")
    except Exception as e:
        print(f"Error: {e}")

#Devolver Libro y calcular multa

def devolver_libro():

    try:
        if not Prestamos:
            print("No hay préstamos registrados.")
            return

        identificacion=input("Ingrese la identificación del usuario: ")
        titulo=input("Ingrese el título del libro a devolver: ")

        prestamo_encontrado = next((p for p in Prestamos if p["usuario"] == identificacion and p["libro"] == titulo and not p["devuelto"]), None)

        if not prestamo_encontrado:
            print("Préstamo no encontrado o ya devuelto.")
            return

        from datetime import datetime
        fecha_actual = datetime.now()
        fecha_limite = datetime.strptime(prestamo_encontrado["fecha_limite"], "%d/%m/%Y")

        dias_atraso = (fecha_actual - fecha_limite).days
        multa = 0

        if dias_atraso > 0:
            multa = dias_atraso * multa_por_dia
            print(f"El libro se devolvió con {dias_atraso} días de retraso \n Multa a pagar:$ {multa} pesos.")

        prestamo_encontrado["devuelto"] = True
        libro_encontrado = next((l for l in Libros if l["titulo"] == titulo), None)
        if libro_encontrado:
            libro_encontrado["disponibles"] += 1
            devolucion=datetime.now()
            devolucion.strftime("%d/%m/%Y %H:%M")

        print("Libro devuelto exitosamente.")

    except ValueError:
        print("Error: Formato de fecha inválido.")

    except Exception as e:
        print(f"Error: {e}")

#Consultar Prestamos
def consultar_prestamos():
    if not Prestamos:
        print("No hay préstamos registrados.")
        return

    print("\nPréstamos registrados:")
    for prestamo in Prestamos:
        print(f"ID: {prestamo['id']}, \n Usuario: {prestamo['usuario']}, \n Libro: {prestamo['libro']}, \n Fecha de préstamo: {prestamo['fecha_prestamo']},Fecha de devolucion: {prestamo['devolucion']}, \n Fecha límite: {prestamo['fecha_limite']}, \n Devuelto: {'Sí' if prestamo['devuelto'] else 'No'}")

#Menu principal
def menu():
    while True:

        try:

            
            print("\n----Menú de Biblioteca----")
            print("1. Registrar Usuario")
            print("2. Registrar Libro")
            print("3. Consultar libro")
            print("4. Prestar libro")
            print("5. Devolver libro")
            print("6. Consultar préstamos")
            print("7. Salir")

            opcion = int(input("Seleccione una opción: "))

            match opcion:
                case 1:
                    registrar_usuario()
                case 2:
                    registrar_libro()
                case 3:
                    consultar_libros()
                case 4:
                    prestar_libro()
                case 5:
                    devolver_libro()
                case 6:
                    consultar_prestamos()
                case 7:
                    print("Saliendo del programa...")
                    break
                case _:
                    print("Opción inválida. Por favor, seleccione una opción dentro del rango mostrado.")
                    
        except ValueError:
            print("Error: Por favor, ingrese un valor válido.")
        except Exception as e:
            print(f"Error inesperado: {e}")

#Ejecutamos el menu
menu()
