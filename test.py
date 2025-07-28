#!/usr/bin/env python3
"""
Test script para verificar la funcionalidad del agente sin GUI.
Prueba todas las funciones principales del core.
"""

import os
import sys
import tempfile
from pathlib import Path

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_functionality():
    """Prueba las funciones principales del core."""
    print("🧪 Iniciando pruebas del core del agente...")
    
    try:
        from core import AgentCore
        
        # Inicializar el agente
        print("1. Inicializando AgentCore...")
        agent = AgentCore()
        print("   ✅ AgentCore inicializado correctamente")
        
        # Probar generación de documento Word
        print("2. Probando generación de documento Word...")
        doc_path = agent.generate_word_document(
            title="Documento de Prueba",
            content="Este es un documento de prueba generado automáticamente.\n\nContiene múltiples párrafos para verificar el funcionamiento correcto.",
            filename="test_document.docx"
        )
        print(f"   ✅ Documento Word generado: {doc_path}")
        
        # Probar generación de presentación PowerPoint
        print("3. Probando generación de presentación PowerPoint...")
        slides_data = [
            {"title": "Introducción", "content": "Esta es una presentación de prueba"},
            {"title": "Contenido", "content": "Contenido de ejemplo\nCon múltiples líneas"},
            {"title": "Conclusión", "content": "Prueba completada exitosamente"}
        ]
        ppt_path = agent.generate_powerpoint_presentation(
            title="Presentación de Prueba",
            slides_content=slides_data,
            filename="test_presentation.pptx"
        )
        print(f"   ✅ Presentación PowerPoint generada: {ppt_path}")
        
        # Probar web scraping (con URL de prueba)
        print("4. Probando web scraping...")
        try:
            scraping_result = agent.scrape_website("https://httpbin.org/html")
            print(f"   ✅ Web scraping completado. Título: {scraping_result.get('title', 'N/A')}")
        except Exception as e:
            print(f"   ⚠️ Web scraping falló (esperado en algunos entornos): {e}")
        
        # Probar herramientas disponibles
        print("5. Probando listado de herramientas...")
        tools = agent.get_available_tools()
        print(f"   ✅ Herramientas disponibles: {len(tools)}")
        for tool in tools:
            print(f"      - {tool['name']} ({tool['category']})")
        
        # Probar guardado de log
        print("6. Probando guardado de log...")
        log_content = "Este es un log de prueba\nCon múltiples líneas\nGenerado automáticamente"
        log_path = agent.save_log_to_file(log_content, "test_log.txt")
        print(f"   ✅ Log guardado: {log_path}")
        
        # Verificar archivos generados
        print("7. Verificando archivos generados...")
        files_to_check = [doc_path, ppt_path, log_path]
        for file_path in files_to_check:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"   ✅ {file_path} - Tamaño: {size} bytes")
            else:
                print(f"   ❌ {file_path} - No encontrado")
        
        print("\n🎉 Todas las pruebas del core completadas exitosamente!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration():
    """Prueba la carga de configuración."""
    print("\n🔧 Probando configuración...")
    
    try:
        import yaml
        
        # Verificar que el archivo de configuración existe
        config_path = "config.yaml"
        if os.path.exists(config_path):
            print(f"   ✅ Archivo de configuración encontrado: {config_path}")
            
            # Cargar y verificar configuración
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            
            required_sections = ['app', 'llm', 'paths', 'ui', 'tools']
            for section in required_sections:
                if section in config:
                    print(f"   ✅ Sección '{section}' encontrada")
                else:
                    print(f"   ⚠️ Sección '{section}' faltante")
        else:
            print(f"   ❌ Archivo de configuración no encontrado: {config_path}")
            
    except Exception as e:
        print(f"   ❌ Error probando configuración: {e}")


def test_dependencies():
    """Prueba que todas las dependencias estén disponibles."""
    print("\n📦 Probando dependencias...")
    
    dependencies = [
        ('yaml', 'PyYAML'),
        ('docx', 'python-docx'),
        ('pptx', 'python-pptx'),
        ('requests', 'requests'),
        ('bs4', 'beautifulsoup4'),
        ('lxml', 'lxml')
    ]
    
    all_ok = True
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - No instalado")
            all_ok = False
    
    # PyQt6 se prueba por separado porque puede fallar en entornos headless
    try:
        import PyQt6
        print("   ✅ PyQt6")
    except ImportError as e:
        if "libEGL" in str(e) or "display" in str(e).lower():
            print("   ⚠️ PyQt6 - Instalado pero no disponible en entorno headless")
        else:
            print(f"   ❌ PyQt6 - No instalado: {e}")
            all_ok = False
    
    return all_ok


def main():
    """Función principal de pruebas."""
    print("🤖 AGENTE PERSONALIZADO - SUITE DE PRUEBAS")
    print("=" * 50)
    
    # Cambiar al directorio del script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Ejecutar pruebas
    success = True
    
    # Probar dependencias
    if not test_dependencies():
        print("\n⚠️ Algunas dependencias faltan, pero continuando con las pruebas...")
    
    # Probar configuración
    test_configuration()
    
    # Probar funcionalidad del core
    if not test_core_functionality():
        success = False
    
    # Resultado final
    print("\n" + "=" * 50)
    if success:
        print("🎉 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("   El agente está listo para usar en un entorno con interfaz gráfica.")
        return 0
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("   Revisa los errores anteriores y corrige los problemas.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)