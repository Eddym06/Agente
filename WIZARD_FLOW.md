## Asistente de Configuración - Capturas de Flujo

Este documento describe la experiencia del usuario con el nuevo asistente de configuración.

### Primera Ejecución

Cuando el usuario ejecuta `python main.py` por primera vez (o cuando falta configuración), aparece automáticamente el asistente:

#### Página 1: Bienvenida
- Título: "¡Bienvenido al Agente Personalizado!"
- Explica que necesita configurar un proveedor LLM
- Lista las opciones disponibles (OpenAI vs LM Studio)

#### Página 2: Selección de Proveedor
- Radio buttons para elegir:
  - OpenAI (GPT-3.5, GPT-4) - con descripción de características
  - LM Studio (Modelos Locales) - con descripción de características

#### Página 3A: Configuración OpenAI (si se eligió OpenAI)
- Campo para API Key (tipo password)
- Campo para modelo (pre-rellenado con gpt-3.5-turbo)
- Link de ayuda a platform.openai.com

#### Página 3B: Configuración LM Studio (si se eligió LM Studio)  
- Campo para URL del servidor (pre-rellenado con http://localhost:1234/v1)
- Campo para nombre del modelo (pre-rellenado con local-model)
- Nota sobre tener LM Studio ejecutándose

#### Página 4: Resumen
- Muestra la configuración elegida
- Para OpenAI: proveedor, API key censurada, modelo
- Para LM Studio: proveedor, URL, modelo
- Botón "Finalizar" para guardar

### Resultado
- Configuración guardada en config.yaml automáticamente
- Mensaje de éxito
- La aplicación principal se inicia normalmente
- No más intervención manual requerida

### Configuración Posterior
- Disponible desde el menú de la aplicación
- Mismo asistente, pero con valores actuales pre-rellenados
- Permite cambiar entre proveedores fácilmente