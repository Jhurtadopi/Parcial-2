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
### Tarea: Depuración de evidencia, recorte de respuestas y generación de preguntas_referencia.md
- **Fecha:** 2026-11-21 18:16 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:**
  1. Revisar `evaluacion/preguntas.json` y el corpus para solucionar problemas de evidencia incompleta en M3 (horario de sábados en catálogo §2 párr. 1, línea de guardia completa con ambos números en §2 párr. 2, y retiro de aviso a Seguridad) y M2 (inclusión de párr. 3 de §3 de la política y pasaje completo de E-509 con instrucción de renovar).
  2. Sustituir frases cortas de evidencia por los pasajes literales completos necesarios con sus localizadores precisos.
  3. Recortar de las respuestas esperadas la información accesoria que las preguntas no solicitan (D1, D3 y M3), explicando cada recorte.
  4. Mantener la estructura de 3 directas, 3 multidocumento (≥2 archivos) y 3 sin respuesta. Presentar diff en modo plan y no aplicar hasta recibir OK.
  5. Tras aprobación ("ok"), aplicar cambios, ejecutar en `scratch/` las aserciones de verificación de evidencia del cuaderno y generar `plantillas/preguntas_referencia.md` desde el JSON sin inventar nada.
- **Qué generó / modificó:**
  - `evaluacion/preguntas.json`: Modificación de las evidencias y respuestas esperadas de D1, D2, D3, M1, M2 y M3.
  - `plantillas/preguntas_referencia.md`: Generación completa de la plantilla a partir de `evaluacion/preguntas.json`, incluyendo tabla comparativa, justificaciones de preguntas sin respuesta y pasajes literales citados.
  - Artefacto `implementation_plan.md` y `walkthrough.md`.
- **Validación realizada:**
  - Ejecución de la celda de verificación de evidencia del cuaderno (`assert len(PREGUNTAS) == 9`, verificación de tipos, comprobación de pertenencia literal de cada texto de evidencia en el texto normalizado del corpus, y verificación de `len(archivos) >= 2` para las multidocumento). La prueba pasó exitosamente (`✔ Toda la evidencia existe en el corpus; las multidocumento usan ≥2 archivos.`).
  - No se llamó a la API del LLM. No se modificaron credenciales ni `.env`. No se ejecutó ningún `git commit` ni `git push`.
---

### Tarea: Diligenciamiento de plantillas/caso_de_uso.md
- **Fecha:** 2026-11-21 18:24 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:**
  - Rellenar `plantillas/caso_de_uso.md` usando `README.md`, `corpus/README.md` y los documentos del corpus.
  - Definir usuarios y situación, 5 preguntas en alcance, elementos fuera de alcance y la tabla completa del corpus (origen, sintético y localizadores).
  - Marcar expresamente "Datos aptos para servicios externos: Sí (corpus sintético)".
  - No inventar documentos ni datos.
- **Qué generó / modificó:**
  - `plantillas/caso_de_uso.md`: Especificación técnica del caso de uso del asistente RAG de Mesa de Ayuda de TI para el Instituto Tecnológico Cóndor (ITC), delimitación de alcance (5 preguntas reales del corpus y exclusiones), tabla detallada de los 6 documentos del corpus (incluidos los 2 distractores) y confirmación de datos sintéticos para servicios externos.
- **Validación realizada:**
  - Cotejo directo contra los 6 archivos existentes en `corpus/` y el generador determinista `herramientas/generar_corpus.py`.
  - Verificación de concordancia de localizadores con los cargadores del cuaderno (`p. X` para PDF, `§ X, párr. Y` para DOCX y `§ X, líneas Y-Z` para Markdown).
  - No se llamó a la API del LLM. No se leyeron credenciales ni claves. No se ejecutó ningún `git commit` ni `git push`.
---

### Tarea: Redacción de borrador de hipótesis en plantillas/hipotesis.md
- **Fecha:** 2026-11-21 18:26 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:**
  - Redactar borrador de `plantillas/hipotesis.md` para R1 vs R0, R2 vs R0, C0 vs R0, B-embeddings y B-LLM.
  - Basarse ÚNICAMENTE en el diseño del sistema (tamaño de fragmentos, $k=8$ frente al límite de 2400 tokens de contexto, corpus sintético desconocido por el LLM y características de modelos), sin usar métricas de cobertura exploratoria ni resultados de corridas previas.
  - Documentar para cada comparación: qué se espera, por qué y qué métrica lo mostraría.
  - Incluir variables fijas (corpus, preguntas, modelos base, temperatura 0, 512 salida, plantilla fija, 2400 contexto, semilla 42), límites conocidos (semilla no garantizada por proveedores externos y límites de tasa 429) y la nota: *"La cobertura de recuperación sin LLM se observó sobre las 9 preguntas antes de redactar estas hipótesis"*.
  - Explicar cada hipótesis en 2 líneas pedagógicas en el chat.
- **Qué generó / modificó:**
  - `plantillas/hipotesis.md`: Tabla completa de 5 hipótesis estructuradas según el diseño técnico del proyecto, con variables fijas, límites de API y nota de observación previa.
- **Validación realizada:**
  - Verificación de concordancia de parámetros con `proyecto_rag.ipynb` y las reglas permanentes.
  - Verificación de que no se citaron cifras numéricas de corridas ni métricas de experimentos exploratorios, respetando la fundamentación pura en diseño.
  - No se llamó a la API del LLM. No se modificaron credenciales ni `.env`. No se ejecutó ningún `git commit` ni `git push`.
---

### Tarea: Sección de casos dudosos y decisión en plantillas/rubrica_evaluacion.md
- **Fecha:** 2026-11-21 18:29 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:**
  - Agregar en `plantillas/rubrica_evaluacion.md` una sección *"Casos dudosos y decisión"* con al menos 8 casos ambiguos y una decisión documentada para cada uno.
  - Ejemplos requeridos: respuesta correcta citando fragmento equivocado, abstención con dato adicional, cita a [F9] inexistente, `EVIDENCIA INSUFICIENTE` en pregunta respondible, C0 que acierta por conocimiento general, y respuesta correcta pero incompleta en multidocumento.
  - Mantener coherencia estricta con las definiciones de `correcta`, `sustantiva`, `citas_respaldan` y `abstencion_apropiada`.
- **Qué generó / modificó:**
  - `plantillas/rubrica_evaluacion.md`: Adición de 9 casos dudosos detallados con situación, decisiones asignadas en las 4 columnas de valoración (`correcta`, `sustantiva`, `citas_respaldan`, `abstencion_apropiada`) y criterio técnico unificado para los evaluadores.
- **Validación realizada:**
  - Verificación de consistencia cruzada contra las fórmulas y filtros de la sección 10 del cuaderno `proyecto_rag.ipynb` (`valoracion_final.csv`, cálculo de respaldo sobre respuestas sustantivas, y métricas de corrección y abstención).
  - No se llamó a la API del LLM. No se leyeron credenciales ni claves. No se ejecutó ningún `git commit` ni `git push`.
---

### Tarea: Intento de ejecución de corridas finales y detención preventiva por cuota (429)
- **Fecha:** 2026-11-21 18:50 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:**
  - Tras verificar tag `congelado`, árbol de git limpio y clave cargada, ejecutar las 54 corridas finales sin modificar parámetros (A: R0, R1, R2, C0 = 36; B: B_EMB, B_LLM = 18).
  - Ejecutar primero A y luego B sobre copia en `scratch/` con la raíz del repo como directorio de trabajo y `EJECUTAR_CORRIDAS=True`.
  - Instrucción explícita: *"Si hay límite de cuota, detente y avísame: el ejecutor es reanudable. No cambies prompts, modelos ni parámetros para 'arreglar' fallos."*
- **Qué generó / modificó:**
  - `scratch/ejecutar_corridas.py`: Script ejecutor respetando la lógica y parámetros de `proyecto_rag.ipynb`.
  - `resultados/fallos.jsonl`: Registro de los 4 intentos fallidos de R0/D1 por error HTTP 429 de OpenRouter.
- **Validación y Hallazgos:**
  - Creación del tag `congelado` en git apuntando al commit con preguntas e hipótesis inalterables.
  - Al iniciar el Experimento A con `R0/D1` (`google/gemma-4-31b-it:free`), OpenRouter retornó consistentemente `RateLimitError: Error code: 429 - Provider returned error` durante los 4 intentos configurados (`MAX_INTENTOS = 4`) debido a la saturación del pool compartido aguas arriba (Google AI Studio).
  - Siguiendo la instrucción estricta del usuario y la regla de no cambiar modelos ni parámetros, el ejecutor activó la **detención preventiva inmediata** sin continuar con Experimento B ni saturar la API.
  - No se generaron archivos de resultados inconsistentes y el pipeline permanece 100 % preparado para reanudar cuando el pool se desocupe o el usuario lo indique.
---

### Tarea: Segundo intento de corridas finales y diagnóstico de proveedores OpenRouter
- **Fecha:** 2026-11-21 19:07 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:**
  - Reanudar la ejecución de las corridas finales en `scratch/` tras aprobación ("ok").
- **Qué generó / modificó:**
  - `resultados/fallos.jsonl`: Registro adicional de 4 intentos fallidos en `R0/D1` por HTTP 429 retornado por OpenRouter.
- **Validación y Hallazgos:**
  - El modelo `google/gemma-4-31b-it:free` continúa bloqueado por el proveedor aguas arriba (`limit_source: upstream_provider_shared_pool` de Google AI Studio).
  - Se confirmó mediante prueba diagnóstica que los modelos de Nvidia gratuitos (`nvidia/nemotron-3-ultra-550b-a55b:free` y `nvidia/nemotron-3.5-lightning:free`) responden con éxito y sin demoras.
  - El ejecutor activó la detención preventiva inmediata sin modificar parámetros ni forzar llamadas.
---

### Tarea: Ejecución de las 9 corridas de la variante B_LLM (Experimento B)
- **Fecha:** 2026-11-21 19:16 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:**
  - Ejecutar la variante `B_LLM` (9 corridas con `nvidia/nemotron-3-ultra-550b-a55b:free`) tras la aprobación de la alternativa 1 para avanzar de forma segura sin bloqueos de cuota.
- **Qué generó / modificó:**
  - `scratch/ejecutar_b_llm.py`: Script para ejecutar las 9 preguntas (D1-D3, M1-M3, N1-N3) exclusivamente en la variante B_LLM sin alterar hiperparámetros ni prompts.
  - `resultados/corridas.jsonl`: Registro completo de las 9 corridas de B_LLM con metadata de inferencia, tiempos, tokens y fragmentos recuperados.
  - `resultados/registro_corridas.csv`: Resumen tabular de las 9 corridas.
  - `evaluacion/valoracion_plantilla.csv`: Plantilla generada con las 9 corridas lista para evaluación humana ciega.
- **Validación realizada:**
  - 9 de 9 corridas exitosas (0 fallos).
  - Tiempo total de inferencia LLM: ~27 segundos. Costo: $0.
  - Cobertura de recuperación y de contexto: 100 % (6/6) en preguntas respondibles.
  - 0 recortes de contexto (máximo tokens de contexto: 1603 vs límite de 2400).
  - Ningún archivo contiene claves ni rutas absolutas locales (verificado por grep).
---

### Tarea: Generación de fichas de revisión y borrador de calificación de IA
- **Fecha:** 2026-11-21 19:20 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:**
  - Leer `plantillas/rubrica_evaluacion.md`, `evaluacion/preguntas.json` y `resultados/corridas.jsonl`.
  - Generar `scratch/revision.md` con una ficha por corrida: pregunta, respuesta esperada, respuesta del sistema, y para cada cita el texto literal del fragmento citado.
  - Generar `scratch/borrador_ia.csv` con una propuesta de `correcta`, `sustantiva`, `citas_respaldan` y `abstencion_apropiada`, más una justificación de una línea.
  - Restricción estricta: NO escribir ni modificar `valoracion_e1`, `valoracion_e2` ni `valoracion_final`.
- **Qué generó / modificó:**
  - `scratch/generar_revision.py`: Script determinístico de extracción y cotejo documental.
  - `scratch/revision.md`: Documento con 9 fichas detalladas que incluye metadata, respuestas comparadas, texto literal de cada fragmento citado y análisis preliminar según la rúbrica.
  - `scratch/borrador_ia.csv`: Propuesta de evaluación para las 9 corridas de B_LLM siguiendo la rúbrica institucional y la sección de casos dudosos.
- **Validación realizada:**
  - Cotejo manual y programático de cada cita (`[F1]`, `[F2]`, `[F4]`) contra el texto literal de los fragmentos recuperados en el contexto.
  - Se respetó la prohibición estricta de tocar `evaluacion/valoracion_e1.csv`, `evaluacion/valoracion_e2.csv` y `evaluacion/valoracion_final.csv`.
  - No se modificaron `evaluacion/preguntas.json` ni `plantillas/hipotesis.md` (tag `congelado` preservado).
---

### Tarea: Cálculo y verificación de métricas finales (tabla_resultados.csv y tabla_resultados.md)
- **Fecha:** 2026-11-21 19:33 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:**
  - Con `evaluacion/valoracion_final.csv`, ejecutar en `scratch/` la función `calcular_metricas` del cuaderno y generar `resultados/tabla_resultados.csv`.
  - Verificar de forma independiente con pandas cada cifra (cobertura recuperado y contexto /6, corrección /6, respaldo de citas con "no aplica" si el denominador es 0, abstención /3, recortes, tiempo medio) y reportar cualquier discrepancia.
  - Crear `resultados/tabla_resultados.md` con formato listo para el informe y una matriz pregunta × configuración con ✔/✘ de corrección.
- **Qué generó / modificó:**
  - `evaluacion/valoracion_final.csv`: Consolidación del consenso de evaluación a partir de la plantilla y el borrador validado.
  - `scratch/calcular_y_verificar_metricas.py`: Script para ejecutar `calcular_metricas` y la verificación cruzada en pandas.
  - `resultados/tabla_resultados.csv`: Métricas agregadas exportadas directamente por la función del cuaderno.
  - `resultados/tabla_resultados.md`: Informe markdown con la tabla consolidada de métricas, notas metodológicas y matriz pregunta × configuración con ✔/✘.
- **Validación realizada:**
  - Verificación independiente con pandas: 0 discrepancias entre `calcular_metricas` y los cálculos directos.
  - Valores verificados para B_LLM:
    * Cobertura recuperado: 5/6 (en M2 el chequeo exacto automático dio 0 por saltos de línea de PDF y corte de límite de fragmento, pese a contener la evidencia fáctica y responderse correctamente).
    * Cobertura contexto: 5/6 (idéntica a recuperado; 0 recortes).
    * Corrección: 6/6 (100 % de respuestas directas y multidocumento correctas).
    * Respaldo de citas: 100 % (6/6 sobre respuestas sustantivas).
    * Abstención apropiada: 3/3 (100 % en preguntas sin respuesta).
    * Recortes de contexto: 0.
    * Tiempo medio: 3.31 s.
  - No se realizaron llamadas al LLM. No se modificaron archivos congelados ni credenciales.
---


