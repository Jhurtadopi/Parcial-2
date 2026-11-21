# Bitácora de Uso de Inteligencia Artificial

Registro de interacciones con asistentes de IA para el proyecto RAG (Mesa de Ayuda de TI - Instituto Tecnológico Cóndor).
Este documento sirve de evidencia para la **Sección 11 del Informe Final: Declaración de uso de IA** (herramientas utilizadas, uso específico y validación de aportes).

---

## Registro de Tareas

### Tarea: Fase 0 - Reglas y Preparación
- **Fecha:** 2026-11-20 18:14 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:** 
  - Añadir a `.gitignore`: `.agent/`, `.gemini/`, `scratch/`.
  - Configurar las reglas permanentes del workspace del proyecto RAG (8 reglas: seguridad de credenciales, inmutabilidad de parámetros y preguntas/hipótesis tras congelación, control de llamadas a LLM, política de commits por el usuario, uso de `scratch/`, explicación pedagógica y bitácora de IA).
- **Qué generó / modificó:**
  - Actualización de `.gitignore` para ignorar `.agent/`, `.gemini/` y `scratch/`.
  - Creación de `AGENTS.md` en la raíz del proyecto y réplicas en `.agent/rules/AGENTS.md` y `.gemini/rules/AGENTS.md`.
  - Creación de las carpetas de trabajo `scratch/` e `informe/`.
  - Creación e inicialización de esta bitácora (`informe/bitacora_ia.md`).
- **Validación realizada:**
  - Verificación de sintaxis de `.gitignore` con `git status`.
  - Comprobación de que `.env` y claves permanecen protegidas y no tocadas.
  - Comprobación de que no se ejecutó ningún `git commit` ni `git push`.
  - Verificación de la lectura y coherencia con `README.md`, `PLAN_TRABAJO.md` y `Enunciado_Proyecto_RAG.md`.

---

### Tarea: Verificación de pipeline y diagnóstico previo (Fase 1 de pruebas)
- **Fecha:** 2026-11-20 18:45 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:** 
  1. Crear `evaluacion/preguntas_desarrollo.json` con 4 preguntas nuevas (2 directas, 1 multidocumento, 1 sin respuesta) con evidencia literal verificada contra el corpus.
  2. Preparar en `scratch/` la prueba de 3 llamadas al LLM (R0, C0, B_LLM) con una pregunta de desarrollo, presentando el plan y esperando confirmación previa.
  3. Diagnóstico sin LLM:
     a) Tokens de contexto y fragmentos recortados en R2 ($k=8$).
     b) Causa de falla de cobertura en M1, M2 y M3 para B_EMB (`bge-m3`) con rangos y puntajes de evidencia vs recuperados.
  4. Resumen en `resultados/diagnostico_previo.md`.
- **Qué generó / modificó:**
  - `evaluacion/preguntas_desarrollo.json` (4 preguntas nuevas verificadas con aserciones Python contra el corpus).
  - `resultados/diagnostico_previo.md` (informe técnico completo con tablas de tokens de R2 y rankings de B_EMB).
  - Copia de seguridad del cuaderno en `scratch/proyecto_rag_prueba.ipynb`.
  - Script de prueba `scratch/probar_3_llamadas.py`.
- **Validación realizada:**
  - Verificación por script de que cada fragmento de evidencia existe de forma exacta en el texto normalizado del corpus.
  - Ejecución local del tokenizador y de los modelos de embeddings (`multilingual-e5-small` y `bge-m3`) para obtener las matrices exactas de similitud y conteos de tokens.
  - No se realizó ninguna llamada a la API del LLM todavía (respetando la regla 4 y solicitando el OK del usuario con el plan detallado).
  - No se ejecutó ningún `git commit` ni `git push`.
---

### Tarea: Prueba de 3 llamadas al LLM en scratch/ (Fase 1 completada)
- **Fecha:** 2026-11-21 17:54 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:** 
  - Ejecutar 3 llamadas con la pregunta de desarrollo `DEV_D2` en `scratch/` bajo las configuraciones R0, C0 y B_LLM tras obtener aprobación explícita ("ok").
  - Reportar: respuesta, citas, abstención detectada, tiempo, modelo reportado y verificación de si alguna respuesta vino vacía (especialmente Nemotron con razonamiento desactivado).
- **Qué generó / modificó:**
  - Creación de `.env` en local vinculando la clave de OpenRouter de forma segura (sin imprimirla ni subirla a git).
  - Ejecución de `scratch/probar_3_llamadas.py`.
- **Validación y Hallazgos:**
  - **B_LLM (`nvidia/nemotron-3-ultra-550b-a55b:free`):** Éxito total. Respondió en 1.075 s con la cita correcta `[F1] manual_conectividad_vpn.pdf · p. 1-2` respaldando el texto literal. No vino vacía (`vino_vacio = False`), demostrando que Nemotron funciona adecuadamente con razonamiento desactivado (`{"reasoning": {"enabled": False}}`).
  - **R0 y C0 (`google/gemma-4-31b-it:free`):** Error HTTP 429 retornado por OpenRouter (`limit_source: upstream_provider_shared_pool` en Google AI Studio por saturación temporal del pool gratuito compartido).
  - Verificación de modelos gratuitos disponibles reportados por OpenRouter: `nvidia/nemotron-3-ultra-550b-a55b:free`, `google/gemma-4-26b-a4b-it:free`, etc.
  - Ningún archivo de producción fuera de `scratch/` ni `.env` fue modificado indebidamente. No se realizaron git commits.
---
