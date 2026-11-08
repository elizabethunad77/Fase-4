# Sistema Integral de Gestion de clientes, servicios y reservas#





import logging
from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# ==========================================
logging.basicConfig(
    filename='sistema.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# ==========================================
# EXCEPCIONES PERSONALIZADAS Y ENCADENAMIENTO
# ==========================================
class ErrorSistemaFJ(Exception):
    """Excepción base para el sistema Software FJ."""
    pass

class ErrorClienteInvalido(ErrorSistemaFJ):
    """Excepción lanzada cuando los datos del cliente no son válidos."""
    pass

class ErrorServicioNoDisponible(ErrorSistemaFJ):
    """Excepción lanzada cuando un servicio no está disponible o los parámetros fallan."""
    pass

class ErrorReservaInvalida(ErrorSistemaFJ):
    """Excepción lanzada ante intentos de reserva incorrectos o inconsistentes."""
    pass

# ==========================================
# CLASE ABSTRACTA BASE
# ==========================================
class EntidadSistema(ABC):
    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def validar_datos(self):
        pass

# ==========================================
# CLASE CLIENTE CON ENCAPSULACIÓN Y VALIDACIÓN
# ==========================================
class Cliente(EntidadSistema):
    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.validar_datos()

    def validar_datos(self):
        try:
            if not self.nombre or len(self.nombre.strip()) < 3:
                raise ValueError("El nombre del cliente es muy corto o está vacío.")
            if "@" not in self.correo or "." not in self.correo:
                raise ValueError("El formato del correo electrónico no es válido.")
            if not self.telefono.isdigit() or len(self.telefono) < 7:
                raise ValueError("El teléfono debe contener solo dígitos y al menos 7 caracteres.")
        except ValueError as e:
            logging.error(f"Fallo de validación en Cliente ID {self.identificador}: {e}")
            raise ErrorClienteInvalido(f"Error al registrar cliente: {e}") from e

# ==========================================
# CLASE ABSTRACTA SERVICIO (POLIMORFISMO)
# ==========================================
class Servicio(ABC):
    def __init__(self, codigo: str, nombre_servicio: str, tarifa_base: float):
        self.codigo = codigo
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        pass

# SERVICIO 1: Reserva de Salas
class ReservaSala(Servicio):
    def __init__(self, codigo: str, tarifa_base: float, capacidad_personas: int):
        super().__init__(codigo, "Reserva de Sala", tarifa_base)
        self.capacidad_personas = capacidad_personas

    # Método sobrecargado mediante argumentos opcionales / kwargs
    def calcular_costo(self, horas: int, descuento_porcentaje: float = 0.0) -> float:
        try:
            if horas <= 0:
                raise ValueError("El número de horas debe ser mayor a cero.")
            subtotal = self.tarifa_base * horas
            descuento = subtotal * (descuento_porcentaje / 100)
            total = subtotal - descuento
            return total
        except Exception as e:
            logging.error(f"Error calculando costo de Sala: {e}")
            raise ErrorServicioNoDisponible("No se pudo calcular el costo de la sala.") from e

    def obtener_descripcion(self) -> str:
        return f"Reserva de Sala (Capacidad: {self.capacidad_personas} personas)"

# SERVICIO 2: Alquiler de Equipos
class AlquilerEquipo(Servicio):
    def __init__(self, codigo: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(codigo, "Alquiler de Equipo", tarifa_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias: int, seguro_adicional: bool = False) -> float:
        try:
            if dias <= 0:
                raise ValueError("Los días de alquiler deben ser mayores a cero.")
            costo_seguro = 15.0 if seguro_adicional else 0.0
            total = (self.tarifa_base * dias) + costo_seguro
            return total
        except Exception as e:
            logging.error(f"Error calculando costo de Equipo: {e}")
            raise ErrorServicioNoDisponible("No se pudo calcular el alquiler del equipo.") from e

    def obtener_descripcion(self) -> str:
        return f"Alquiler de Equipo tecnológico tipo: {self.tipo_equipo}"

# SERVICIO 3: Asesorías Especializadas
class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo: str, tarifa_base: float, area_experto: str):
        super().__init__(codigo, "Asesoría Especializada", tarifa_base)
        self.area_experto = area_experto

    def calcular_costo(self, sesiones: int, impuesto_iva: float = 1.19) -> float:
        try:
            if sesiones <= 0:
                raise ValueError("El número de sesiones debe ser mayor a cero.")
            total = (self.tarifa_base * sesiones) * impuesto_iva
            return total
        except Exception as e:
            logging.error(f"Error calculando costo de Asesoría: {e}")
            raise ErrorServicioNoDisponible("No se pudo calcular la asesoría.") from e

    def obtener_descripcion(self) -> str:
        return f"Asesoría en el área de: {self.area_experto}"
