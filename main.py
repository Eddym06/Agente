"""
Main Module - Punto de entrada de la aplicación
Configura y arranca el agente personalizado con interfaz PyQt6.
"""

import sys
import os
import logging
from pathlib import Path

# Añadir el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QIcon
except ImportError as e:
    print(f"Error: PyQt6 no está instalado. Instala las dependencias con: pip install -r requirements.txt")
    print(f"Detalles del error: {e}")
    sys.exit(1)

try:
    from ui import AgentUI, create_application
    from core import AgentCore
except ImportError as e:
    print(f"Error importando módulos: {e}")
    sys.exit(1)


def setup_logging():
    """
    Configura el sistema de logging global de la aplicación.
    """
    # Crear directorio de logs si no existe
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'application.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Logger específico para la aplicación
    logger = logging.getLogger('AgentApp')
    logger.info("Sistema de logging inicializado")
    return logger


def check_dependencies():
    """
    Verifica que todas las dependencias estén instaladas.
    
    Returns:
        tuple: (success: bool, missing_deps: list)
    """
    required_modules = [
        ('PyQt6', 'PyQt6'),
        ('docx', 'python-docx'),
        ('pptx', 'python-pptx'),
        ('requests', 'requests'),
        ('bs4', 'beautifulsoup4'),
        ('yaml', 'PyYAML')
    ]
    
    missing_deps = []
    
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
        except ImportError:
            missing_deps.append(package_name)
    
    return len(missing_deps) == 0, missing_deps


def create_directories():
    """
    Crea los directorios necesarios para la aplicación.
    """
    directories = [
        './documents',
        './presentations', 
        './logs',
        './temp'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)


def show_startup_info():
    """
    Muestra información de inicio en la consola.
    """
    print("=" * 60)
    print("🤖 AGENTE PERSONALIZADO")
    print("=" * 60)
    print("Versión: 1.0.0")
    print("Desarrollado con PyQt6 y Python")
    print("Iniciando interfaz gráfica...")
    print("=" * 60)


def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Maneja excepciones no capturadas de manera elegante.
    
    Args:
        exc_type: Tipo de excepción
        exc_value: Valor de la excepción
        exc_traceback: Traceback de la excepción
    """
    if issubclass(exc_type, KeyboardInterrupt):
        # Permitir Ctrl+C para cerrar
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger = logging.getLogger('AgentApp')
    logger.error("Excepción no capturada", exc_info=(exc_type, exc_value, exc_traceback))
    
    # Mostrar diálogo de error si hay una aplicación Qt activa
    app = QApplication.instance()
    if app:
        error_msg = f"Error inesperado: {exc_value}\n\nConsulta los logs para más detalles."
        QMessageBox.critical(None, "Error", error_msg)


def main():
    """
    Función principal de la aplicación.
    """
    try:
        # Mostrar información de inicio
        show_startup_info()
        
        # Configurar logging
        logger = setup_logging()
        logger.info("Iniciando Agente Personalizado...")
        
        # Verificar dependencias
        deps_ok, missing_deps = check_dependencies()
        if not deps_ok:
            error_msg = f"Dependencias faltantes: {', '.join(missing_deps)}\n"
            error_msg += "Instala las dependencias con: pip install -r requirements.txt"
            print(f"Error: {error_msg}")
            return 1
        
        logger.info("Todas las dependencias están disponibles")
        
        # Crear directorios necesarios
        create_directories()
        logger.info("Directorios de trabajo creados")
        
        # Configurar manejo de excepciones
        sys.excepthook = handle_exception
        
        # Configurar aplicación Qt
        # Habilitar alta DPI
        #QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        #QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # Crear aplicación
        app = create_application()
        logger.info("Aplicación Qt creada")
        
        # Configurar icono si existe
        icon_path = "icon.png"
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
        
        # Crear y mostrar ventana principal
        try:
            main_window = AgentUI()
            main_window.show()
            logger.info("Interfaz gráfica iniciada correctamente")
            
            print("✅ Agente Personalizado iniciado correctamente")
            print("📋 La interfaz gráfica está ahora disponible")
            print("🔄 Usa Ctrl+C en la consola para cerrar la aplicación")
            
        except Exception as e:
            logger.error(f"Error creando la interfaz: {e}")
            QMessageBox.critical(None, "Error de Inicio", 
                               f"No se pudo iniciar la interfaz gráfica:\n{str(e)}\n\n"
                               f"Verifica que todas las dependencias estén instaladas correctamente.")
            return 1
        
        # Ejecutar bucle principal de la aplicación
        return app.exec()
        
    except KeyboardInterrupt:
        print("\n🛑 Aplicación interrumpida por el usuario")
        return 0
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        return 1
    finally:
        print("👋 Cerrando Agente Personalizado...")


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
