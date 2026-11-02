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
