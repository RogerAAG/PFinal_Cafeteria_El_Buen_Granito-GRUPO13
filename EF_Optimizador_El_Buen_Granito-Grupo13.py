import json
import random

def cargar_datos_desde_json(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return [] if nombre_archivo == 'empleados.json' else {}
    except json.JSONDecodeError:
        print(f"Error: El archivo {nombre_archivo} está mal formado.")
        return [] if nombre_archivo == 'empleados.json' else {}

def visualizar_empleados(lista_para_mostrar):
    print("\n--- LISTA DE EMPLEADOS ---")
    if not lista_para_mostrar:
        print("No hay empleados registrados.")
        return

    for i, empleado in enumerate(lista_para_mostrar, 1):
        print(f"{i}. Nombre: {empleado['nombre']}, DNI: {empleado['dni']}, No disponible: {empleado['disponibilidad_no']}")


def agregar_empleado():
    print("\n--- AGREGAR NUEVO EMPLEADO ---")
    nombre = input("Nombre completo del empleado: ")
    dni = input("DNI del empleado: ")
    dias_no_str = input("Días no disponibles separados por coma (ej: Lunes,Martes): ")
    disponibilidad_no = [dia.strip() for dia in dias_no_str.split(',')]

    nuevo_empleado = {
        "nombre": nombre,
        "dni": dni,
        "disponibilidad_no": disponibilidad_no
    }

    print(f"¡Empleado '{nombre}' listo para ser agregado!")
    return nuevo_empleado

def gestionar_empleados(lista_de_empleados):
    while True:
        print("\n--- GESTIÓN DE EMPLEADOS ---")
        print("1. Ver lista de Empleados")
        print("2. Agregar nuevo Empleado")
        print("3. Volver al Menú Principal")

        sub_opcion = input("Elige una opción: ")

        if sub_opcion == '1':
            visualizar_empleados(lista_de_empleados)
        elif sub_opcion == '2':
            empleado_nuevo = agregar_empleado()
            lista_de_empleados.append(empleado_nuevo)
            print("¡Empleado agregado a la lista con éxito!")
        elif sub_opcion == '3':
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción no válida.")


def guardar_datos(lista_de_empleados, horario):
    try:
        with open('empleados.json', 'w') as archivo_emp:
            json.dump(lista_de_empleados, archivo_emp, indent=4)

        if horario:
            with open('horario.json', 'w') as archivo_hor:
                json.dump(horario, archivo_hor, indent=4)

        print("✅ ¡Datos guardados correctamente!")
    except Exception as e:
        print(f"❌ Error al guardar los datos: {e}")

def crear_estructura_horario():
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    horario = {dia: {"Mañana": None, "Tarde": None} for dia in dias_semana}
    return horario


def generar_horario(lista_de_empleados):
    print("\n⏳ Iniciando la generación del horario...")

    if not lista_de_empleados:
        print("❌ No se puede generar un horario porque no hay empleados registrados.")
        return None

    horario_semanal = crear_estructura_horario()

    if resolver_horario_backtracking(lista_de_empleados, horario_semanal):
        print("✅ ¡Horario generado con éxito!")
        return horario_semanal
    else:
        print("❌ No se pudo encontrar una solución de horario con los empleados y restricciones actuales.")
        return None

def visualizar_horario(horario):
    print("\n--- HORARIO SEMANAL ---")
    if not horario:
        print("Aún no se ha generado un horario. Usa la opción 2.")
        return

    for dia, turnos in horario.items():
        print(f"\n--- {dia.upper()} ---")
        mañana = turnos.get("Mañana", "Libre")
        tarde = turnos.get("Tarde", "Libre")

        print(f"  Mañana (8am-4pm): {mañana if mañana else 'Sin asignar'}")
        print(f"  Tarde  (2pm-10pm): {tarde if tarde else 'Sin asignar'}")


def es_asignacion_valida(empleado, dia, horario):
    """Verifica si un empleado está disponible para trabajar en un día específico."""
    if dia in empleado["disponibilidad_no"]:
        return False
    return True

def resolver_horario_backtracking(lista_de_empleados, horario):
    """Implementación del algoritmo de backtracking para encontrar una solución
    de horario válida."""
    # Itera sobre cada día y turno para encontrar una celda vacía
    for dia, turnos in horario.items():
        for turno, asignado in turnos.items():
            if asignado is None:  # Encuentra el primer turno sin asignar

                # Baraja los empleados para introducir aleatoriedad y equidad
                empleados_barajados = lista_de_empleados[:]
                random.shuffle(empleados_barajados)

                for empleado in empleados_barajados:
                    # Verifica si la asignación es posible
                    if es_asignacion_valida(empleado, dia, horario):
                        # Asigna tentativamente al empleado
                        horario[dia][turno] = empleado["nombre"]

                        # Llamada recursiva para resolver el resto del horario
                        if resolver_horario_backtracking(lista_de_empleados, horario):
                            return True  # ¡Solución encontrada!

                        # Backtrack: si la recursión falla, deshace la asignación
                        horario[dia][turno] = None

                return False  # No se encontró empleado para este turno

    return True  # El horario está completo

if __name__ == "__main__":

    empleados = cargar_datos_desde_json('empleados.json')
    horario_actual = cargar_datos_desde_json('horario.json')

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Gestionar Empleados")
        print("2. Generar Nuevo Horario")
        print("3. Ver Horario Actual")
        print("4. Guardar Cambios")
        print("5. Salir")

        opcion = input("Elige una opción (1-5): ")

        if opcion == '1':
            gestionar_empleados(empleados)
        elif opcion == '2':
            horario_actual = generar_horario(empleados)
        elif opcion == '3':
            visualizar_horario(horario_actual)
        elif opcion == '4':
            # Ahora pasa ambos datos a la función de guardado
            guardar_datos(empleados, horario_actual)
        elif opcion == '5':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elige un número del 1 al 5.")