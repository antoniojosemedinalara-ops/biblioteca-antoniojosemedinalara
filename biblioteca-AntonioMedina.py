# variables globales 
#Establecemos las variables globales
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
        #Ingresamos los dtos del usuario
        print("Registro de usuario")
        nombre=input("Ingrese el nombre del usuario: ")
        identificacion=input("Ingrese la identificación del usuario: ")
        edad=int(input("Ingrese la edad del usuario: "))

        while edad <= 0 or edad > 120:
            print("Error: Por favor, ingrese una edad válida.")

            edad=int(input("Ingrese la edad del usuario: "))

        #Se reemplazan los datos en  el diccionario de usuario

        usuario={
            "nombre":nombre,
            "identificacion":identificacion,
            "edad":edad
        }

        Usuarios.append(usuario)#Los datos se añaden a su lista general
        print("Usuario registrado exitosamente.")

    except ValueError:
        print("Error: Por favor, ingrese una edad válida.")
    except Exception as e:
        print(f"Error: {e}")

#Registro de Libros
def registrar_libro():
    try:
        #Ingresamos los datos del libro
        print("Registro de libro")
        titulo=input("Ingrese el título del libro: ")
        autor=input("Ingrese el autor del libro: ")
        cantidad=int(input("Ingrese la cantidad de ejemplares: "))

        #Se reemplazan los datos en  el diccionario del libro

        libro={
            "titulo":titulo,
            "autor":autor,
            "cantidad":cantidad,
            "disponibles":cantidad
        }

        Libros.append(libro)#Los datos se añaden a la lista general
        print("Libro registrado exitosamente.")

    except ValueError:
        print("Error: Por favor, ingrese una cantidad válida.")
    except Exception as e:
        print(f"Error: {e}")

#Consulta de Libros

def consultar_libros():
    #Se comprueba si hay libros en la lista
    if not Libros:
        print("No hay libros registrados.")
        return

    print("Libros disponibles:")
    #se muestran uno a uno los datos del diccionario o diccionarios que se ingresaron
    for libro in Libros: 
        print(f"Título: {libro['titulo']}, \n Autor: {libro['autor']}, \n Cantidad: {libro['cantidad']}, \n Disponibles: {libro['disponibles']}")

#Prestar Libro
def prestar_libro():
    try:
        #se comprueba si hay usuarios en la lista
        if not Usuarios:
            print("No hay usuarios registrados. Por favor, registre un usuario primero.")
            return
        #se comprueba si hay libros en la lista
        if not Libros:
            print("No hay libros registrados. Por favor, registre un libro primero.")
            return

        identificacion=input("Ingrese la identificación del usuario: ")

        #se busca de uno en uno los datos ingresados en la lista hasta que coincidan con el ingresado anteriormente
        usuario_encontrado = next((u for u in Usuarios if u["identificacion"] == identificacion), None)

        if not usuario_encontrado:
            print("Usuario no encontrado. Por favor, intente nuevamente.")#No coincidio con el ingresado
            return

        titulo=input("Ingrese el título del libro a prestar: ")
        #se busca de uno en uno los datos ingresados en la lista hasta que coincidan con el ingresado anteriormente
        libro_encontrado = next((l for l in Libros if l["titulo"] == titulo), None)

        if not libro_encontrado:
            print("Libro no encontrado. Por favor, registre el libro primero.")#No coincidio
            return
        
        #Se verifica lacantidad de libros
        if libro_encontrado["disponibles"] == 0:
            print("No hay ejemplares disponibles para este libro.")
            return

        #Se usan las intrucciones datetime y timedelta para ingresar las fechas y poder modificarlas
        from datetime import datetime, timedelta
        fecha_prestamo = datetime.now() #Se ingresa la fecha actual del computador
        fecha_limite = fecha_prestamo + timedelta(days=dias_prestamo) # con la fecha actual,timedelta y los dias de prestamo establecemos la fecha limite
        #Creamos un diccionario para prestamos
        prestamo={
            "id": len(Prestamos) + 1,
            "usuario": identificacion,
            "libro": titulo,
            #Se establecen como se van a organizar las fechas del prestamo y limite
            "fecha prestamo": fecha_prestamo.strftime("%d/%m/%Y"),
            "fecha limite": fecha_limite.strftime("%d/%m/%Y"),
            "devuelto": False
        }

        Prestamos.append(prestamo) #Se añaden a la lista
        libro_encontrado["disponibles"] -= 1 # se restan la cantidad disponible 
        print(f"Libro prestado exitosamente. Fecha límite de devolución: {fecha_limite.strftime('%d/%m/%Y')}")
    except Exception as e:
        print(f"Error: {e}")

#Devolver Libro y calcular multa

def devolver_libro():

    try:
        #Se comprueba si hay prestamos ingresados
        if not Prestamos:
            print("No hay préstamos registrados.")
            return

        identificacion=input("Ingrese la identificación del usuario: ")
        titulo=input("Ingrese el título del libro a devolver: ")
        #Se buscan uno a uno si estan en la lista los datos ingresados
        prestamo_encontrado = next((p for p in Prestamos if p["usuario"] == identificacion and p["libro"] == titulo and not p["devuelto"]), None)

        if not prestamo_encontrado:
            print("Préstamo no encontrado o ya devuelto.")#No se encontraron
            return
        # Se vuelve a usar la instruccion datetime 
        from datetime import datetime
        fecha_actual = datetime.now()
        fecha_limite = datetime.strptime(prestamo_encontrado["fecha_limite"], "%d/%m/%Y")#Se comprueba con strptime la fecha limite

        dias_atraso = (fecha_actual - fecha_limite).days #Se restan para comprobar si hay dias de retraso
        multa = 0
        #Se excedio de la fecha limite
        if dias_atraso > 0: 
            multa = dias_atraso * multa_por_dia #Se multiplican los dias  de retraso con la multa por dia
            print(f"El libro se devolvió con {dias_atraso} días de retraso \n Multa a pagar:$ {multa} pesos.")
        #Entrego a tiempo el libro
        prestamo_encontrado["devuelto"] = True
        libro_encontrado = next((l for l in Libros if l["titulo"] == titulo), None)#se busca en la lista por los titulos hasta encontrar
        if libro_encontrado:
            libro_encontrado["disponibles"] += 1 #Se suma y se añade de vuelta las unidades disponibles 
            devolucion=datetime.now()
            devolucion.strftime("%d/%m/%Y %H:%M")
            

        print("Libro devuelto exitosamente.")

    except ValueError:
        print("Error: Formato de fecha inválido.")

    except Exception as e:
        print(f"Error: {e}")

#Consultar Prestamos
def consultar_prestamos():
    #Se comprueba si hay prestamos disponibles
    if not Prestamos:
        print("No hay préstamos registrados.")
        return
    
    print("\nPréstamos registrados:")
    for prestamo in Prestamos:
        print(f"ID: {prestamo['id']}, \n Usuario: {prestamo['usuario']}, \n Libro: {prestamo['libro']}, \n Fecha de préstamo: {prestamo['fecha prestamo']},Fecha de devolucion: {prestamo['devolucion']}, \n Fecha límite: {prestamo['fecha limite']}, \n Devuelto: {'Sí' if prestamo['devuelto'] else 'No'}")

#Menu principal
def menu():
    while True:

        try:

            #Se crea un menu con match-case con las funciones 
            
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
