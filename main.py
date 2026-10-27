from datetime import datetime
#este es la actualizacion del archivo
class Estacionamiento:
    def __init__(self, total_lugares):
        self.total_lugares = total_lugares
        # Diccionario de tarifas por hora según el tipo de vehículo
        self.tarifas = {
            "moto": 15.0,
            "auto": 30.0,
            "camioneta": 45.0
        }
        # Diccionario para llevar el control de los vehículos dentro: {placa: {"tipo": tipo, "hora_ingreso": datetime}}
        self.vehiculos_activos = {}

    def consultar_disponibilidad(self):
        """Muestra los lugares totales, ocupados y disponibles en tiempo real."""
        ocupados = len(self.vehiculos_activos)
        disponibles = self.total_lugares - ocupados
        
        print("\n" + "="*30)
        print("    ESTADO DEL ESTACIONAMIENTO")
        print("="*30)
        print(f" Lugares totales:     {self.total_lugares}")
        print(f" Lugares ocupados:    {ocupados}")
        print(f" Lugares disponibles: {disponibles}")
        print("="*30)
        return disponibles

    def registrar_ingreso(self, placa, tipo_vehiculo):
        """Registra la entrada de un vehículo si hay espacio y el tipo es válido."""
        placa = placa.upper().strip()
        tipo_vehiculo = tipo_vehiculo.lower().strip()

        if placa in self.vehiculos_activos:
            print(f"\n[Error] El vehículo con placa {placa} ya se encuentra registrado dentro.")
            return False

        if tipo_vehiculo not in self.tarifas:
            print(f"\n[Error] Tipo de vehículo no válido. Opciones: {list(self.tarifas.keys())}")
            return False

        if len(self.vehiculos_activos) >= self.total_lugares:
            print("\n[Lo siento] El estacionamiento está lleno. No hay lugares disponibles.")
            return False

        # Registrar ingreso con la hora actual
        hora_ingreso = datetime.now()
        self.vehiculos_activos[placa] = {
            "tipo": tipo_vehiculo,
            "hora_ingreso": hora_ingreso
        }
        
        print(f"\n[Éxito] Vehículo {placa} ({tipo_vehiculo}) registrado a las {hora_ingreso.strftime('%H:%M:%S')}.")
        self.consultar_disponibilidad()
        return True

    def registrar_salida(self, placa):
        """Registra la salida del vehículo, calcula el tiempo y el monto a pagar."""
        placa = placa.upper().strip()

        if placa not in self.vehiculos_activos:
            print(f"\n[Error] No se encontró ningún vehículo activo con la placa {placa}.")
            return None

        # Obtener datos de ingreso
        datos = self.vehiculos_activos.pop(placa)
        tipo = datos["tipo"]
        hora_ingreso = datos["hora_ingreso"]
        hora_salida = datetime.now()

        # Calcular tiempo transcurrido
        diferencia = hora_salida - hora_ingreso
        horas_totales = diferencia.total_seconds() / 3600
        
        # Cobro mínimo de 1 hora o fracción redondeada hacia arriba (puedes ajustar esta lógica)
        if horas_totales < 0.01: 
            horas_cobro = 1.0  # Por seguridad si sale inmediatamente
        else:
            import math
            horas_cobro = math.ceil(horas_totales)

        tarifa_hora = self.tarifas[tipo]
        total_pagar = horas_cobro * tarifa_hora

        print("\n" + "="*30)
        print("          TICKET DE SALIDA")
        print("="*30)
        print(f" Placa:            {placa}")
        print(f" Tipo:             {tipo.capitalize()}")
        print(f" Hora de ingreso:  {hora_ingreso.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f" Hora de salida:   {hora_salida.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f" Tiempo estadias:  {diferencia}")
        print(f" Horas a cobrar:   {int(horas_cobro)}")
        print(f" Tarifa por hora:  ${tarifa_hora:.2f}")
        print(f" TOTAL A PAGAR:    ${total_pagar:.2f}")
        print("="*30)
        
        self.consultar_disponibilidad()
        return total_pagar


# --- Ejemplo de uso interactivo ---
if __name__ == "__main__":
    # Creamos un estacionamiento con capacidad para 5 lugares
    mi_estacionamiento = Estacionamiento(total_lugares=5)

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrar ingreso de vehículo")
        print("2. Registrar salida y cobro")
        print("3. Ver disponibilidad en tiempo real")
        print("4. Salir")
        
        opcion = input("Elige una opción (1-4): ").strip()

        if opcion == "1":
            placa = input("Ingresa la placa del vehículo: ")
            tipo = input("Ingresa el tipo (auto / moto / camioneta): ")
            mi_estacionamiento.registrar_ingreso(placa, tipo)
        elif opcion == "2":
            placa = input("Ingresa la placa del vehículo que sale: ")
            mi_estacionamiento.registrar_salida(placa)
        elif opcion == "3":
            mi_estacionamiento.consultar_disponibilidad()
        elif opcion == "4":
            print("\n¡Gracias por usar el sistema de estacionamiento!")
            break
        else:
            print("\n[Opción inválida] Por favor, elige un número del 1 al 4.")
