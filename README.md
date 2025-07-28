# 🤖 Agente Personalizado

Un agente inteligente con interfaz gráfica moderna desarrollado en Python con PyQt6. Incluye herramientas avanzadas para automatización de documentos, web scraping, integración con modelos de lenguaje (LLM) y más.

## ✨ Características

### 🎨 Interfaz Gráfica
- **Diseño moderno y profesional** con modo oscuro
- **Interfaz responsive** y minimalista
- **Threading** para mantener la UI reactiva
- **Logger en tiempo real** con coloreado de sintaxis
- **Panel de control** con botones configurables

### 🛠️ Herramientas Incluidas
- **Generación de documentos**: Word (.docx) y PowerPoint (.pptx)
- **Web Scraping**: Extracción de datos de sitios web
- **Integración LLM**: Compatible con LM Studio y OpenAI API
- **Procesamiento de texto**: Análisis, resumen y mejora con IA
- **Gestión de configuración**: Archivos YAML/JSON
- **Sistema de logs**: Registro detallado de actividades

### 🔧 Arquitectura Modular
- **Separación clara**: UI, lógica de negocio y configuración
- **Código bien documentado** y comentado
- **Gestión de errores** robusta
- **Compatible** con Windows y macOS

## 📋 Requisitos

### Sistema
- Python 3.8 o superior
- Windows 10/11 o macOS 10.14+
- Mínimo 4GB RAM
- 500MB espacio libre en disco

### Dependencias Python
```
PyQt6==6.6.1
python-docx==1.1.0
python-pptx==0.6.23
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.4
openai==1.12.0
PyYAML==6.0.1
packaging==23.2
```

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/Eddym06/Agente.git
cd Agente
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv agent_env

# Windows
agent_env\Scripts\activate

# macOS/Linux
source agent_env/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
python main.py
```

**¡Listo!** En el primer arranque, la aplicación detectará automáticamente que falta configuración y mostrará un **asistente de configuración** que te guiará paso a paso para:

- Seleccionar tu proveedor LLM preferido (OpenAI o LM Studio)
- Introducir los datos necesarios (API key, modelos, URLs)
- Guardar la configuración automáticamente

**No necesitas editar archivos manualmente.** Todo se configura desde la interfaz gráfica.

## 🐳 Compatibilidad con Docker

El agente mantiene total compatibilidad con Docker y entornos virtuales. El asistente de configuración se adapta automáticamente al entorno de ejecución.

## 🎯 Uso

### Configuración Inicial

La primera vez que ejecutes la aplicación, aparecerá automáticamente un **Asistente de Configuración** que te guiará para:

1. **Seleccionar el proveedor LLM:**
   - **OpenAI**: Para usar GPT-3.5, GPT-4, etc.
   - **LM Studio**: Para usar modelos locales

2. **Configurar los parámetros:**
   - **OpenAI**: Introducir API key y seleccionar modelo
   - **LM Studio**: Configurar URL del servidor y nombre del modelo

3. **Guardar la configuración** automáticamente en `config.yaml`

### Iniciar la aplicación
```bash
python main.py
```

Si necesitas cambiar la configuración posteriormente, ve a la interfaz y accede al menú de configuración.

### Interfaz Principal

La aplicación se divide en tres áreas principales:

#### 1. **Panel de Control** (izquierda)
- **📄 Generación de Documentos**
  - Generar Documento Word
  - Generar Presentación PowerPoint
- **🌐 Herramientas Web**
  - Web Scraping
  - Análisis de Datos Web
- **🤖 Herramientas IA**
  - Consulta LLM
  - Procesamiento de Texto

#### 2. **Área Principal** (derecha)
- **💬 Entrada de Texto**: Escribe consultas o instrucciones
- **📋 Salida y Logs**: Visualiza resultados y actividad del sistema

#### 3. **Header**
- Título de la aplicación
- Indicador de estado en tiempo real

### Ejemplos de Uso

#### Generar Documento Word
1. Escribe el contenido en el área de entrada
2. Haz clic en "Generar Documento Word"
3. El archivo se guardará en `./documents/`

#### Consultar LLM
1. Escribe tu pregunta en el área de entrada
2. Haz clic en "🚀 Procesar con IA"
3. La respuesta aparecerá en la pestaña "Resultados"

#### Web Scraping
1. Haz clic en "Web Scraping"
2. Los datos extraídos se mostrarán en formato estructurado

## ⚙️ Configuración

### Archivo config.yaml

```yaml
# Configuración de la aplicación
app:
  name: "Agente Personalizado"
  version: "1.0.0"
  theme: "dark"

# Configuración de LLM
llm:
  provider: "lm_studio"  # "lm_studio" o "openai"
  lm_studio:
    base_url: "http://localhost:1234/v1"
    model: "local-model"
  openai:
    api_key: ""  # Tu API key de OpenAI
    model: "gpt-3.5-turbo"

# Rutas de archivos
paths:
  documents_output: "./documents"
  presentations_output: "./presentations"
  logs: "./logs"
  temp: "./temp"

# Configuración de la interfaz
ui:
  window:
    title: "Agente Personalizado - Control Panel"
    width: 1200
    height: 800
  colors:
    primary: "#2D3748"
    accent: "#3182CE"
    background: "#1A202C"
    # ... más colores
```

### Integración con LM Studio

1. **Instalar LM Studio** desde [lmstudio.ai](https://lmstudio.ai)
2. **Descargar un modelo** (recomendado: Llama 2 7B o similar)
3. **Iniciar el servidor local** en el puerto 1234
4. **Ejecutar el agente**: El asistente de configuración te guiará para configurar la conexión automáticamente

### Integración con OpenAI

1. **Obtener API Key** desde [platform.openai.com](https://platform.openai.com)
2. **Ejecutar el agente**: El asistente de configuración te pedirá la API key y te permitirá seleccionar el modelo

### Reconfiguración

Si necesitas cambiar la configuración posteriormente:
- Desde la interfaz: Menú → Configuración
- Manual: Edita `config.yaml` directamente (opcional)

## 📁 Estructura del Proyecto

```
Agente/
├── main.py              # Punto de entrada de la aplicación
├── ui.py                # Interfaz gráfica PyQt6
├── core.py              # Lógica de negocio y herramientas
├── config.yaml          # Configuración de la aplicación
├── requirements.txt     # Dependencias Python
├── README.md           # Esta documentación
├── documents/          # Documentos Word generados
├── presentations/      # Presentaciones PowerPoint generadas
├── logs/              # Archivos de log
└── temp/              # Archivos temporales
```

## 🔧 Personalización

### Añadir Nuevas Herramientas

1. **En core.py**, añade tu función:
```python
def mi_nueva_herramienta(self, parametros):
    """Tu nueva funcionalidad."""
    # Implementación
    return resultado
```

2. **En config.yaml**, registra la herramienta:
```yaml
tools:
  mi_categoria:
    - name: "Mi Nueva Herramienta"
      description: "Descripción de la herramienta"
      enabled: true
```

3. **En ui.py**, añade el manejador si es necesario.

### Personalizar Colores

Modifica la sección `ui.colors` en `config.yaml`:
```yaml
ui:
  colors:
    primary: "#tu-color-primario"
    accent: "#tu-color-acento"
    # ... otros colores
```

## 🐛 Solución de Problemas

### Error: "PyQt6 no está instalado"
```bash
pip install PyQt6
```

### Error: "No module named 'docx'"
```bash
pip install python-docx python-pptx
```

### La aplicación no inicia
1. Verifica que Python 3.8+ esté instalado
2. Asegúrate de que todas las dependencias estén instaladas
3. Revisa los logs en `./logs/application.log`

### LLM no responde
1. **LM Studio**: Verifica que el servidor esté corriendo en localhost:1234
2. **OpenAI**: Verifica tu API key y saldo disponible
3. Revisa la configuración en `config.yaml`

### Documentos no se generan
1. Verifica permisos de escritura en las carpetas
2. Asegúrate de que las carpetas de salida existan
3. Revisa los logs para errores específicos

## 📝 Logs y Debugging

### Ubicación de Logs
- **Aplicación**: `./logs/application.log`
- **Agente**: `./logs/agent.log`

### Niveles de Log
- `DEBUG`: Información detallada
- `INFO`: Información general
- `WARNING`: Advertencias
- `ERROR`: Errores

### Configurar Nivel de Log
En `config.yaml`:
```yaml
logging:
  level: "DEBUG"  # DEBUG, INFO, WARNING, ERROR
```

## 🚀 Funciones Avanzadas

### Threading
La aplicación usa threading para:
- Mantener la UI responsive durante operaciones largas
- Ejecutar consultas LLM sin bloquear la interfaz
- Procesar archivos grandes en segundo plano

### Sistema de Plugins
Puedes extender la funcionalidad añadiendo:
- Nuevas herramientas en `core.py`
- Configuraciones en `config.yaml`
- Integraciones con APIs externas

### Exportación de Datos
- **Documentos**: Formato Word (.docx)
- **Presentaciones**: Formato PowerPoint (.pptx)
- **Logs**: Formato texto (.txt)
- **Datos**: Formato JSON para scraping

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Add nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/Eddym06/Agente/issues)
- **Documentación**: Este README y comentarios en el código
- **Email**: Contacta al desarrollador para soporte adicional

## 🗺️ Roadmap

### Versión 1.1
- [ ] Sistema de plugins más robusto
- [ ] Integración con más LLMs
- [ ] Temas de UI personalizables
- [ ] Exportación a más formatos

### Versión 1.2
- [ ] Base de datos SQLite para historial
- [ ] Interfaz web opcional
- [ ] Integración con servicios cloud
- [ ] Análisis de sentimientos

---

**🎉 ¡Disfruta usando el Agente Personalizado!**

*Desarrollado con ❤️ en Python y PyQt6*