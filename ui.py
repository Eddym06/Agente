"""
UI Module - Interfaz gráfica con PyQt6
Implementa una interfaz moderna, responsive y profesional con modo oscuro.
Incluye threading para mantener la UI reactiva y logging en tiempo real.
"""

import sys
import os
import threading
import traceback
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QScrollArea,
    QFrame, QSplitter, QProgressBar, QMessageBox, QFileDialog,
    QGroupBox, QTabWidget, QComboBox, QSpinBox, QCheckBox, QWizard, 
    QWizardPage, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QSize, QPropertyAnimation, 
    QEasingCurve, pyqtSlot
)
from PyQt6.QtGui import (
    QFont, QPalette, QColor, QPixmap, QIcon, QTextCursor, 
    QSyntaxHighlighter, QTextCharFormat
)

from core import AgentCore


class WorkerThread(QThread):
    """
    Hilo de trabajo para ejecutar tareas en segundo plano.
    Evita bloquear la interfaz durante operaciones largas.
    """
    
    # Señales para comunicación con la UI
    progress_updated = pyqtSignal(str)  # Mensaje de progreso
    task_completed = pyqtSignal(str, object)  # Tarea completada con resultado
    error_occurred = pyqtSignal(str, str)  # Error con mensaje y traceback
    
    def __init__(self, task_func: Callable, *args, **kwargs):
        super().__init__()
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs
        
    def run(self):
        """Ejecuta la tarea en el hilo de trabajo."""
        try:
            self.progress_updated.emit("Iniciando tarea...")
            result = self.task_func(*self.args, **self.kwargs)
            self.task_completed.emit("Tarea completada exitosamente", result)
        except Exception as e:
            error_msg = str(e)
            error_traceback = traceback.format_exc()
            self.error_occurred.emit(error_msg, error_traceback)


class LogHighlighter(QSyntaxHighlighter):
    """
    Resaltador de sintaxis para el área de logs.
    Colorea diferentes tipos de mensajes para mejor legibilidad.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_formats()
    
    def setup_formats(self):
        """Configura los formatos de coloreado."""
        # Formato para INFO
        self.info_format = QTextCharFormat()
        self.info_format.setForeground(QColor("#A0AEC0"))  # Gris claro
        
        # Formato para SUCCESS
        self.success_format = QTextCharFormat()
        self.success_format.setForeground(QColor("#38A169"))  # Verde
        self.success_format.setFontWeight(QFont.Weight.Bold)
        
        # Formato para WARNING
        self.warning_format = QTextCharFormat()
        self.warning_format.setForeground(QColor("#D69E2E"))  # Amarillo
        self.warning_format.setFontWeight(QFont.Weight.Bold)
        
        # Formato para ERROR
        self.error_format = QTextCharFormat()
        self.error_format.setForeground(QColor("#E53E3E"))  # Rojo
        self.error_format.setFontWeight(QFont.Weight.Bold)
        
        # Formato para timestamps
        self.timestamp_format = QTextCharFormat()
        self.timestamp_format.setForeground(QColor("#718096"))  # Gris
        
    def highlightBlock(self, text):
        """Aplica el resaltado al bloque de texto."""
        # Resaltar timestamps
        if text.startswith('['):
            end_bracket = text.find(']')
            if end_bracket != -1:
                self.setFormat(0, end_bracket + 1, self.timestamp_format)
        
        # Resaltar por tipo de mensaje
        if 'ERROR' in text or 'Error' in text:
            self.setFormat(0, len(text), self.error_format)
        elif 'WARNING' in text or 'Warning' in text:
            self.setFormat(0, len(text), self.warning_format)
        elif 'SUCCESS' in text or 'Success' in text or 'completada' in text:
            self.setFormat(0, len(text), self.success_format)
        else:
            self.setFormat(0, len(text), self.info_format)


class ModernButton(QPushButton):
    """
    Botón personalizado con estilo moderno y efectos hover.
    """
    
    def __init__(self, text: str, icon_path: str = None, primary: bool = False):
        super().__init__(text)
        self.primary = primary
        self.setup_style()
        
        if icon_path and os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(20, 20))
    
    def setup_style(self):
        """Configura el estilo del botón."""
        if self.primary:
            style = """
                ModernButton {
                    background-color: #3182CE;
                    color: #F7FAFC;
                    border: 2px solid #3182CE;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: bold;
                }
                ModernButton:hover {
                    background-color: #2B77CB;
                    border-color: #2B77CB;
                }
                ModernButton:pressed {
                    background-color: #2C5AA0;
                }
                ModernButton:disabled {
                    background-color: #4A5568;
                    border-color: #4A5568;
                    color: #A0AEC0;
                }
            """
        else:
            style = """
                ModernButton {
                    background-color: #4A5568;
                    color: #F7FAFC;
                    border: 2px solid #4A5568;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 13px;
                }
                ModernButton:hover {
                    background-color: #718096;
                    border-color: #718096;
                }
                ModernButton:pressed {
                    background-color: #2D3748;
                }
                ModernButton:disabled {
                    background-color: #2D3748;
                    border-color: #2D3748;
                    color: #718096;
                }
            """
        
        self.setStyleSheet(style)
        self.setMinimumHeight(40 if self.primary else 35)


class ConfigurationWizard(QWizard):
    """
    Asistente de configuración inicial para el agente.
    Guía al usuario para configurar el proveedor LLM y sus parámetros.
    """
    
    def __init__(self, config_data: Dict[str, Any] = None):
        super().__init__()
        self.config_data = config_data or {}
        self.setup_wizard()
        
    def setup_wizard(self):
        """Configurar el asistente de configuración."""
        self.setWindowTitle("Configuración Inicial - Agente Personalizado")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        self.setFixedSize(600, 500)
        
        # Páginas del asistente
        self.addPage(WelcomePage())
        self.addPage(ProviderSelectionPage())
        self.addPage(OpenAIConfigPage())
        self.addPage(LMStudioConfigPage())
        self.addPage(SummaryPage())
        
        # Estilos
        self.setStyleSheet("""
            QWizard {
                background-color: #1A202C;
                color: #F7FAFC;
            }
            QWizardPage {
                background-color: #1A202C;
                color: #F7FAFC;
            }
            QLabel {
                color: #F7FAFC;
            }
            QLineEdit {
                background-color: #2D3748;
                border: 2px solid #4A5568;
                border-radius: 4px;
                padding: 8px;
                color: #F7FAFC;
            }
            QLineEdit:focus {
                border-color: #3182CE;
            }
            QRadioButton {
                color: #F7FAFC;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator:unchecked {
                background-color: #2D3748;
                border: 2px solid #4A5568;
                border-radius: 8px;
            }
            QRadioButton::indicator:checked {
                background-color: #3182CE;
                border: 2px solid #3182CE;
                border-radius: 8px;
            }
        """)


class WelcomePage(QWizardPage):
    """Página de bienvenida del asistente."""
    
    def __init__(self):
        super().__init__()
        self.setTitle("¡Bienvenido al Agente Personalizado!")
        self.setSubTitle("Este asistente te ayudará a configurar tu agente por primera vez.")
        
        layout = QVBoxLayout()
        
        welcome_text = QLabel(
            "Para comenzar a usar el agente, necesitas configurar un proveedor de "
            "modelo de lenguaje (LLM). Puedes elegir entre:\n\n"
            "• OpenAI: Usa modelos como GPT-3.5 o GPT-4 (requiere API key)\n"
            "• LM Studio: Usa modelos locales ejecutados en tu equipo\n\n"
            "El asistente te guiará paso a paso para configurar tu opción preferida."
        )
        welcome_text.setWordWrap(True)
        welcome_text.setStyleSheet("font-size: 14px; line-height: 1.6;")
        
        layout.addWidget(welcome_text)
        layout.addStretch()
        
        self.setLayout(layout)


class ProviderSelectionPage(QWizardPage):
    """Página para seleccionar el proveedor LLM."""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Selecciona tu Proveedor LLM")
        self.setSubTitle("Elige cómo quieres usar el modelo de lenguaje.")
        
        layout = QVBoxLayout()
        
        # Grupo de botones radio
        self.provider_group = QButtonGroup()
        
        # Opción OpenAI
        self.openai_radio = QRadioButton("OpenAI (GPT-3.5, GPT-4)")
        self.openai_radio.setChecked(True)
        openai_desc = QLabel("• Modelos de alta calidad\n• Requiere conexión a internet\n• Requiere API key de OpenAI")
        openai_desc.setStyleSheet("margin-left: 25px; color: #A0AEC0; font-size: 12px;")
        
        # Opción LM Studio
        self.lmstudio_radio = QRadioButton("LM Studio (Modelos Locales)")  
        lmstudio_desc = QLabel("• Modelos ejecutados localmente\n• No requiere internet una vez descargado\n• Requiere LM Studio instalado")
        lmstudio_desc.setStyleSheet("margin-left: 25px; color: #A0AEC0; font-size: 12px;")
        
        self.provider_group.addButton(self.openai_radio, 0)
        self.provider_group.addButton(self.lmstudio_radio, 1)
        
        layout.addWidget(self.openai_radio)
        layout.addWidget(openai_desc)
        layout.addSpacing(20)
        layout.addWidget(self.lmstudio_radio)
        layout.addWidget(lmstudio_desc)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Registrar el campo para que el wizard pueda acceder a él
        self.registerField("provider", self.openai_radio)
    
    def nextId(self):
        """Determina qué página mostrar siguiente."""
        if self.openai_radio.isChecked():
            return 2  # OpenAIConfigPage
        else:
            return 3  # LMStudioConfigPage


class OpenAIConfigPage(QWizardPage):
    """Página de configuración para OpenAI."""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Configuración de OpenAI")
        self.setSubTitle("Ingresa tu API key y selecciona el modelo.")
        
        layout = QVBoxLayout()
        
        # API Key
        api_key_label = QLabel("API Key de OpenAI:")
        api_key_label.setStyleSheet("font-weight: bold;")
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("sk-...")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        api_key_help = QLabel("Obtén tu API key en: https://platform.openai.com/api-keys")
        api_key_help.setStyleSheet("color: #A0AEC0; font-size: 11px;")
        
        # Modelo
        model_label = QLabel("Modelo:")
        model_label.setStyleSheet("font-weight: bold;")
        self.model_input = QLineEdit()
        self.model_input.setText("gpt-3.5-turbo")
        self.model_input.setPlaceholderText("gpt-3.5-turbo")
        
        model_help = QLabel("Ejemplos: gpt-3.5-turbo, gpt-4, gpt-4-turbo")
        model_help.setStyleSheet("color: #A0AEC0; font-size: 11px;")
        
        layout.addWidget(api_key_label)
        layout.addWidget(self.api_key_input)
        layout.addWidget(api_key_help)
        layout.addSpacing(20)
        layout.addWidget(model_label)
        layout.addWidget(self.model_input)
        layout.addWidget(model_help)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Registrar campos
        self.registerField("openai_api_key*", self.api_key_input)
        self.registerField("openai_model*", self.model_input)
    
    def nextId(self):
        """Saltar la página de LM Studio."""
        return 4  # SummaryPage


class LMStudioConfigPage(QWizardPage):
    """Página de configuración para LM Studio."""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Configuración de LM Studio")
        self.setSubTitle("Configura la conexión con tu servidor local de LM Studio.")
        
        layout = QVBoxLayout()
        
        # URL base
        url_label = QLabel("URL del Servidor:")
        url_label.setStyleSheet("font-weight: bold;")
        self.url_input = QLineEdit()
        self.url_input.setText("http://localhost:1234/v1")
        self.url_input.setPlaceholderText("http://localhost:1234/v1")
        
        url_help = QLabel("Asegúrate de que LM Studio esté ejecutándose en servidor local")
        url_help.setStyleSheet("color: #A0AEC0; font-size: 11px;")
        
        # Modelo
        model_label = QLabel("Nombre del Modelo:")
        model_label.setStyleSheet("font-weight: bold;")
        self.model_input = QLineEdit()
        self.model_input.setText("local-model")
        self.model_input.setPlaceholderText("local-model")
        
        model_help = QLabel("El nombre puede ser genérico como 'local-model'")
        model_help.setStyleSheet("color: #A0AEC0; font-size: 11px;")
        
        layout.addWidget(url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(url_help)
        layout.addSpacing(20)
        layout.addWidget(model_label)
        layout.addWidget(self.model_input)
        layout.addWidget(model_help)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Registrar campos
        self.registerField("lmstudio_url*", self.url_input)
        self.registerField("lmstudio_model*", self.model_input)


class SummaryPage(QWizardPage):
    """Página de resumen de la configuración."""
    
    def __init__(self):
        super().__init__()
        self.setTitle("Resumen de Configuración")
        self.setSubTitle("Revisa tu configuración antes de guardar.")
        
        layout = QVBoxLayout()
        
        self.summary_label = QLabel()
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("font-size: 14px; background-color: #2D3748; padding: 15px; border-radius: 8px;")
        
        layout.addWidget(self.summary_label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def initializePage(self):
        """Actualizar el resumen cuando se muestra la página."""
        # Obtener la página de selección de proveedor
        provider_page = self.wizard().page(1)
        
        if provider_page.openai_radio.isChecked():
            api_key = self.field("openai_api_key")
            model = self.field("openai_model")
            summary_text = f"""
            <b>Proveedor:</b> OpenAI<br>
            <b>API Key:</b> {'*' * 20 + api_key[-4:] if len(api_key) > 4 else '*' * len(api_key)}<br>
            <b>Modelo:</b> {model}<br><br>
            
            Tu agente usará OpenAI para procesar consultas.
            Asegúrate de que tu API key tenga saldo suficiente.
            """
        else:
            url = self.field("lmstudio_url")
            model = self.field("lmstudio_model")
            summary_text = f"""
            <b>Proveedor:</b> LM Studio<br>
            <b>URL del Servidor:</b> {url}<br>
            <b>Modelo:</b> {model}<br><br>
            
            Tu agente usará un modelo local a través de LM Studio.
            Asegúrate de que LM Studio esté ejecutándose antes de usar el agente.
            """
        
        self.summary_label.setText(summary_text)


class AgentUI(QMainWindow):
    """
    Interfaz principal del agente personalizado.
    Implementa una UI moderna, responsive y profesional.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        super().__init__()
        
        # Inicializar core del agente
        try:
            self.agent_core = AgentCore(config_path)
            self.config = self.agent_core.config
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error inicializando el agente: {str(e)}")
            sys.exit(1)
        
        # Verificar si la configuración es válida
        config_valid, missing_items = self.agent_core.is_config_valid()
        if not config_valid:
            # Mostrar wizard de configuración
            if not self.show_configuration_wizard():
                # Usuario canceló la configuración, cerrar aplicación
                sys.exit(0)
        
        # Variables de control
        self.current_worker = None
        self.log_lines = []
        self.max_log_lines = self.config.get('logging', {}).get('max_lines', 1000)
        
        # Configurar la ventana principal
        self.setup_window()
        self.setup_theme()
        self.setup_ui()
        self.setup_connections()
        
        # Mensaje de bienvenida
        self.add_log("=== AGENTE PERSONALIZADO INICIADO ===", "SUCCESS")
        self.add_log(f"Versión: {self.config['app']['version']}")
        self.add_log(f"Herramientas disponibles: {len(self.agent_core.get_available_tools())}")
    
    def show_configuration_wizard(self) -> bool:
        """
        Muestra el asistente de configuración y procesa los resultados.
        
        Returns:
            bool: True si la configuración fue completada, False si fue cancelada
        """
        wizard = ConfigurationWizard(self.config)
        
        if wizard.exec() == QWizard.DialogCode.Accepted:
            # Procesar la configuración
            try:
                new_config = self.config.copy()
                
                # Obtener página de selección de proveedor
                provider_page = wizard.page(1)
                
                if provider_page.openai_radio.isChecked():
                    # Configuración OpenAI
                    api_key = wizard.field("openai_api_key")
                    model = wizard.field("openai_model")
                    
                    new_config['llm'] = {
                        'provider': 'openai',
                        'openai': {
                            'api_key': api_key,
                            'model': model
                        },
                        'lm_studio': new_config.get('llm', {}).get('lm_studio', {
                            'base_url': 'http://localhost:1234/v1',
                            'model': 'local-model'
                        })
                    }
                else:
                    # Configuración LM Studio
                    url = wizard.field("lmstudio_url")
                    model = wizard.field("lmstudio_model")
                    
                    new_config['llm'] = {
                        'provider': 'lm_studio',
                        'lm_studio': {
                            'base_url': url,
                            'model': model
                        },
                        'openai': new_config.get('llm', {}).get('openai', {
                            'api_key': '',
                            'model': 'gpt-3.5-turbo'
                        })
                    }
                
                # Guardar configuración
                self.agent_core.save_config_to_file(new_config)
                
                QMessageBox.information(self, "Configuración Guardada", 
                                      "La configuración ha sido guardada exitosamente.\n"
                                      "El agente está listo para usar.")
                return True
                
            except Exception as e:
                QMessageBox.critical(self, "Error", 
                                   f"Error guardando la configuración:\n{str(e)}")
                return False
        else:
            # Usuario canceló
            return False
    
    def setup_window(self):
        """Configura la ventana principal."""
        ui_config = self.config.get('ui', {}).get('window', {})
        
        self.setWindowTitle(ui_config.get('title', 'Agente Personalizado'))
        self.setGeometry(100, 100, 
                        ui_config.get('width', 1200), 
                        ui_config.get('height', 800))
        self.setMinimumSize(ui_config.get('min_width', 800), 
                           ui_config.get('min_height', 600))
    
    def setup_theme(self):
        """Configura el tema oscuro y los colores."""
        colors = self.config.get('ui', {}).get('colors', {})
        
        # Configurar paleta de colores
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(colors.get('background', '#1A202C')))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(colors.get('text_primary', '#F7FAFC')))
        palette.setColor(QPalette.ColorRole.Base, QColor(colors.get('surface', '#2D3748')))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors.get('secondary', '#4A5568')))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors.get('surface', '#2D3748')))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors.get('text_primary', '#F7FAFC')))
        palette.setColor(QPalette.ColorRole.Text, QColor(colors.get('text_primary', '#F7FAFC')))
        palette.setColor(QPalette.ColorRole.Button, QColor(colors.get('secondary', '#4A5568')))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors.get('text_primary', '#F7FAFC')))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(colors.get('accent', '#3182CE')))
        palette.setColor(QPalette.ColorRole.Link, QColor(colors.get('accent', '#3182CE')))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors.get('accent', '#3182CE')))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors.get('text_primary', '#F7FAFC')))
        
        self.setPalette(palette)
        
        # Estilo global de la aplicación
        app_style = f"""
            QMainWindow {{
                background-color: {colors.get('background', '#1A202C')};
                color: {colors.get('text_primary', '#F7FAFC')};
            }}
            QWidget {{
                background-color: {colors.get('background', '#1A202C')};
                color: {colors.get('text_primary', '#F7FAFC')};
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }}
            QGroupBox {{
                background-color: {colors.get('surface', '#2D3748')};
                border: 2px solid {colors.get('secondary', '#4A5568')};
                border-radius: 8px;
                margin: 5px;
                padding-top: 15px;
                font-weight: bold;
            }}
            QGroupBox::title {{
                color: {colors.get('text_primary', '#F7FAFC')};
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
            QTextEdit {{
                background-color: {colors.get('surface', '#2D3748')};
                border: 2px solid {colors.get('secondary', '#4A5568')};
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }}
            QLineEdit {{
                background-color: {colors.get('surface', '#2D3748')};
                border: 2px solid {colors.get('secondary', '#4A5568')};
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {colors.get('accent', '#3182CE')};
            }}
            QProgressBar {{
                background-color: {colors.get('secondary', '#4A5568')};
                border: none;
                border-radius: 4px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {colors.get('accent', '#3182CE')};
                border-radius: 4px;
            }}
            QScrollBar:vertical {{
                background-color: {colors.get('secondary', '#4A5568')};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {colors.get('accent', '#3182CE')};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #2B77CB;
            }}
        """
        
        self.setStyleSheet(app_style)
    
    def setup_ui(self):
        """Configura todos los elementos de la interfaz."""
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Crear el splitter principal
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Panel lateral izquierdo
        self.setup_sidebar(main_splitter)
        
        # Panel principal derecho
        self.setup_main_panel(main_splitter)
        
        # Configurar proporciones del splitter
        main_splitter.setSizes([350, 850])
        main_splitter.setCollapsible(0, False)
        main_splitter.setCollapsible(1, False)
    
    def setup_sidebar(self, parent):
        """Configura el panel lateral con controles."""
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(5, 5, 5, 5)
        sidebar_layout.setSpacing(10)
        
        # Header del panel
        header_label = QLabel("PANEL DE CONTROL")
        header_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #3182CE;
                padding: 10px;
                border-bottom: 2px solid #3182CE;
                margin-bottom: 10px;
            }
        """)
        sidebar_layout.addWidget(header_label)
        
        # Área de scroll para botones
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(8)
        
        # Crear botones para herramientas
        self.create_tool_buttons(scroll_layout)
        
        scroll_area.setWidget(scroll_widget)
        sidebar_layout.addWidget(scroll_area)
        
        # Espacio flexible
        sidebar_layout.addStretch()
        
        # Botón de configuración
        config_btn = ModernButton("⚙️ Configuración")
        config_btn.clicked.connect(self.show_configuration)
        sidebar_layout.addWidget(config_btn)
        
        parent.addWidget(sidebar_widget)
    
    def create_tool_buttons(self, layout):
        """Crea los botones para las herramientas disponibles."""
        tools = self.agent_core.get_available_tools()
        
        # Agrupar por categoría
        categories = {}
        for tool in tools:
            category = tool['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(tool)
        
        # Crear botones por categoría
        category_names = {
            'document_generation': '📄 Generación de Documentos',
            'web_tools': '🌐 Herramientas Web',
            'llm_tools': '🤖 Herramientas IA'
        }
        
        for category, tools in categories.items():
            # Grupo de categoría
            group = QGroupBox(category_names.get(category, category.title()))
            group_layout = QVBoxLayout(group)
            group_layout.setSpacing(5)
            
            for tool in tools:
                btn = ModernButton(tool['name'])
                btn.setToolTip(tool['description'])
                btn.clicked.connect(lambda checked, t=tool: self.execute_tool(t))
                group_layout.addWidget(btn)
            
            layout.addWidget(group)
    
    def setup_main_panel(self, parent):
        """Configura el panel principal con entrada de texto y logs."""
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)
        
        # Header principal
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2D3748;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("🤖 AGENTE PERSONALIZADO")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #3182CE;
            }
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Status indicator
        self.status_label = QLabel("● Listo")
        self.status_label.setStyleSheet("color: #38A169; font-weight: bold;")
        header_layout.addWidget(self.status_label)
        
        main_layout.addWidget(header_frame)
        
        # Área de entrada de texto
        input_group = QGroupBox("💬 Entrada de Texto")
        input_layout = QVBoxLayout(input_group)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Escribe tu consulta o instrucción aquí...")
        self.text_input.setMaximumHeight(120)
        input_layout.addWidget(self.text_input)
        
        # Botones de acción para entrada
        input_buttons_layout = QHBoxLayout()
        
        self.process_btn = ModernButton("🚀 Procesar con IA", primary=True)
        self.process_btn.clicked.connect(self.process_text_input)
        input_buttons_layout.addWidget(self.process_btn)
        
        clear_btn = ModernButton("🗑️ Limpiar")
        clear_btn.clicked.connect(self.clear_text_input)
        input_buttons_layout.addWidget(clear_btn)
        
        input_buttons_layout.addStretch()
        input_layout.addLayout(input_buttons_layout)
        
        main_layout.addWidget(input_group)
        
        # Área de salida y logs
        output_group = QGroupBox("📋 Salida y Logs")
        output_layout = QVBoxLayout(output_group)
        
        # Tabs para diferentes tipos de salida
        self.output_tabs = QTabWidget()
        
        # Tab de logs
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Consolas", 11))
        
        # Configurar highlighter para logs
        self.log_highlighter = LogHighlighter(self.log_output.document())
        
        self.output_tabs.addTab(self.log_output, "📄 Logs")
        
        # Tab de resultados
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.output_tabs.addTab(self.result_output, "✨ Resultados")
        
        output_layout.addWidget(self.output_tabs)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        output_layout.addWidget(self.progress_bar)
        
        # Botones de acción para salida
        output_buttons_layout = QHBoxLayout()
        
        save_log_btn = ModernButton("💾 Guardar Log")
        save_log_btn.clicked.connect(self.save_log)
        output_buttons_layout.addWidget(save_log_btn)
        
        clear_log_btn = ModernButton("🗑️ Limpiar Log")
        clear_log_btn.clicked.connect(self.clear_log)
        output_buttons_layout.addWidget(clear_log_btn)
        
        output_buttons_layout.addStretch()
        output_layout.addLayout(output_buttons_layout)
        
        main_layout.addWidget(output_group)
        
        parent.addWidget(main_widget)
    
    def setup_connections(self):
        """Configura las conexiones de señales y slots."""
        # Timer para actualizar el estado
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(5000)  # Cada 5 segundos
    
    # === MÉTODOS DE INTERFAZ ===
    
    def add_log(self, message: str, level: str = "INFO"):
        """
        Añade un mensaje al log con timestamp y nivel.
        
        Args:
            message: Mensaje a añadir
            level: Nivel del mensaje (INFO, SUCCESS, WARNING, ERROR)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}"
        
        # Añadir a la lista de logs
        self.log_lines.append(formatted_message)
        
        # Mantener solo las últimas líneas según configuración
        if len(self.log_lines) > self.max_log_lines:
            self.log_lines = self.log_lines[-self.max_log_lines:]
        
        # Actualizar UI
        self.log_output.clear()
        self.log_output.setPlainText('\n'.join(self.log_lines))
        
        # Scroll automático al final
        cursor = self.log_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_output.setTextCursor(cursor)
    
    def set_status(self, status: str, color: str = "#38A169"):
        """
        Actualiza el indicador de estado.
        
        Args:
            status: Texto del estado
            color: Color del indicador
        """
        self.status_label.setText(f"● {status}")
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
    
    def show_progress(self, show: bool = True):
        """Muestra u oculta la barra de progreso."""
        self.progress_bar.setVisible(show)
        if show:
            self.progress_bar.setRange(0, 0)  # Indeterminado
        else:
            self.progress_bar.setRange(0, 1)
            self.progress_bar.setValue(1)
    
    # === MÉTODOS DE ACCIÓN ===
    
    def execute_tool(self, tool: Dict[str, Any]):
        """
        Ejecuta una herramienta específica.
        
        Args:
            tool: Diccionario con información de la herramienta
        """
        self.add_log(f"Ejecutando: {tool['name']}")
        self.set_status("Procesando...", "#D69E2E")
        self.show_progress(True)
        
        # Deshabilitar botones durante la ejecución
        self.process_btn.setEnabled(False)
        
        # Determinar qué función ejecutar
        if tool['name'] == "Generar Documento Word":
            self.execute_word_generation()
        elif tool['name'] == "Generar Presentación PowerPoint":
            self.execute_powerpoint_generation()
        elif tool['name'] == "Web Scraping":
            self.execute_web_scraping()
        elif tool['name'] == "Consulta LLM":
            self.execute_llm_query()
        elif tool['name'] == "Procesamiento de Texto":
            self.process_text_input()
        else:
            self.add_log(f"Herramienta no implementada: {tool['name']}", "WARNING")
            self.reset_ui_state()
    
    def execute_word_generation(self):
        """Ejecuta la generación de documento Word."""
        def task():
            content = self.text_input.toPlainText() or "Documento generado automáticamente por el agente personalizado."
            return self.agent_core.generate_word_document(
                title="Documento Generado",
                content=content
            )
        
        self.start_worker_task(task, "Generación de documento Word")
    
    def execute_powerpoint_generation(self):
        """Ejecuta la generación de presentación PowerPoint."""
        def task():
            content = self.text_input.toPlainText() or "Presentación generada automáticamente."
            slides = [
                {"title": "Introducción", "content": content},
                {"title": "Contenido Principal", "content": content},
                {"title": "Conclusiones", "content": "Generado por el agente personalizado"}
            ]
            return self.agent_core.generate_powerpoint_presentation(
                title="Presentación Generada",
                slides_content=slides
            )
        
        self.start_worker_task(task, "Generación de presentación PowerPoint")
    
    def execute_web_scraping(self):
        """Ejecuta web scraping."""
        def task():
            # Por defecto usar una URL de ejemplo
            url = "https://httpbin.org/html"  # URL de prueba que siempre funciona
            return self.agent_core.scrape_website(url)
        
        self.start_worker_task(task, "Web scraping")
    
    def execute_llm_query(self):
        """Ejecuta consulta al LLM."""
        text_input = self.text_input.toPlainText().strip()
        if not text_input:
            self.add_log("Por favor, ingresa texto para procesar", "WARNING")
            self.reset_ui_state()
            return
        
        def task():
            return self.agent_core.query_llm(text_input)
        
        self.start_worker_task(task, "Consulta LLM")
    
    def process_text_input(self):
        """Procesa el texto de entrada con IA."""
        text_input = self.text_input.toPlainText().strip()
        if not text_input:
            self.add_log("Por favor, ingresa texto para procesar", "WARNING")
            return
        
        def task():
            return self.agent_core.process_text_with_llm(text_input, "analyze")
        
        self.start_worker_task(task, "Procesamiento de texto con IA")
    
    def start_worker_task(self, task_func: Callable, task_name: str):
        """
        Inicia una tarea en un hilo de trabajo.
        
        Args:
            task_func: Función a ejecutar
            task_name: Nombre descriptivo de la tarea
        """
        # Detener worker anterior si existe
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.terminate()
            self.current_worker.wait()
        
        # Crear nuevo worker
        self.current_worker = WorkerThread(task_func)
        self.current_worker.progress_updated.connect(self.on_worker_progress)
        self.current_worker.task_completed.connect(lambda msg, result: self.on_worker_completed(msg, result, task_name))
        self.current_worker.error_occurred.connect(self.on_worker_error)
        
        # Iniciar tarea
        self.current_worker.start()
    
    @pyqtSlot(str)
    def on_worker_progress(self, message: str):
        """Maneja actualizaciones de progreso del worker."""
        self.add_log(message)
    
    @pyqtSlot(str, object, str)
    def on_worker_completed(self, message: str, result: Any, task_name: str):
        """Maneja la finalización exitosa de una tarea."""
        self.add_log(message, "SUCCESS")
        
        # Mostrar resultado según el tipo
        if isinstance(result, str):
            if result.endswith(('.docx', '.pptx', '.txt')):
                # Es una ruta de archivo
                self.result_output.setPlainText(f"Archivo generado: {result}")
                self.add_log(f"Archivo guardado en: {result}")
            else:
                # Es texto de respuesta
                self.result_output.setPlainText(result)
        elif isinstance(result, dict):
            # Es un diccionario (ej: resultado de scraping)
            formatted_result = self.format_dict_result(result)
            self.result_output.setPlainText(formatted_result)
        else:
            self.result_output.setPlainText(str(result))
        
        # Cambiar a la tab de resultados
        self.output_tabs.setCurrentIndex(1)
        
        self.reset_ui_state()
    
    @pyqtSlot(str, str)
    def on_worker_error(self, error_msg: str, traceback_str: str):
        """Maneja errores del worker."""
        self.add_log(f"Error: {error_msg}", "ERROR")
        self.result_output.setPlainText(f"Error: {error_msg}\n\nDetalles:\n{traceback_str}")
        self.output_tabs.setCurrentIndex(1)
        self.reset_ui_state()
    
    def format_dict_result(self, result: Dict[str, Any]) -> str:
        """Formatea un resultado de diccionario para mostrar."""
        formatted = ""
        for key, value in result.items():
            if isinstance(value, list):
                formatted += f"{key.upper()}:\n"
                for item in value[:5]:  # Mostrar solo los primeros 5 elementos
                    formatted += f"  - {item}\n"
                if len(value) > 5:
                    formatted += f"  ... y {len(value) - 5} más\n"
            elif isinstance(value, str) and len(value) > 200:
                formatted += f"{key.upper()}:\n{value[:200]}...\n\n"
            else:
                formatted += f"{key.upper()}: {value}\n"
        return formatted
    
    def reset_ui_state(self):
        """Resetea el estado de la UI después de completar una tarea."""
        self.set_status("Listo")
        self.show_progress(False)
        self.process_btn.setEnabled(True)
    
    # === MÉTODOS DE UTILIDAD ===
    
    def clear_text_input(self):
        """Limpia el área de entrada de texto."""
        self.text_input.clear()
        self.add_log("Entrada de texto limpiada")
    
    def clear_log(self):
        """Limpia el log."""
        self.log_lines.clear()
        self.log_output.clear()
        self.result_output.clear()
        self.add_log("Log limpiado")
    
    def save_log(self):
        """Guarda el log actual en un archivo."""
        try:
            log_content = '\n'.join(self.log_lines)
            file_path = self.agent_core.save_log_to_file(log_content)
            self.add_log(f"Log guardado en: {file_path}", "SUCCESS")
        except Exception as e:
            self.add_log(f"Error guardando log: {str(e)}", "ERROR")
    
    def show_configuration(self):
        """Muestra el diálogo de configuración."""
        if self.show_configuration_wizard():
            self.add_log("Configuración actualizada exitosamente", "SUCCESS")
        else:
            self.add_log("Configuración cancelada por el usuario", "WARNING")
    
    def update_status(self):
        """Actualiza el estado periódicamente."""
        if not (self.current_worker and self.current_worker.isRunning()):
            self.set_status("Listo")
    
    def closeEvent(self, event):
        """Maneja el cierre de la aplicación."""
        # Detener worker si está corriendo
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.terminate()
            self.current_worker.wait()
        
        self.add_log("Cerrando aplicación...")
        event.accept()


def create_application() -> QApplication:
    """
    Crea y configura la aplicación Qt.
    
    Returns:
        Instancia de QApplication configurada
    """
    app = QApplication(sys.argv)
    app.setApplicationName("Agente Personalizado")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("AgenteDev")
    
    # Configurar fuente global
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    return app


if __name__ == "__main__":
    # Crear aplicación
    app = create_application()
    
    # Crear ventana principal
    window = AgentUI()
    window.show()
    
    # Iniciar bucle de eventos
    sys.exit(app.exec())