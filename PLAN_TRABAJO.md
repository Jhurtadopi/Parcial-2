# Plan de trabajo — Proyecto RAG

## 1. Resumen
- **Caso de uso:** por definir hoy (lun 16). Recomendado: mesa de ayuda de TI de una organización ficticia, con corpus sintético marcado como tal, para que el LLM no conozca las respuestas de memoria y C0 sirva de contraste real.
- **Hoy:** lun 16 nov · **Entrega:** lun 23 nov, 11:59 p.m. (Classroom) · **Meta interna:** lun 23, 6:00 p.m. · **Sustentación:** mié 25 nov · **Días restantes:** 7
- **Camino crítico:** corpus (Julian) → índice R0 (Julian) → R0 de punta a punta (Compañero/a 1) → preguntas e hipótesis congeladas (Compañero/a 2) → corridas finales → calificación y métricas → informe

Julian está en el camino crítico desde el día 1: si el corpus o el índice se atrasan, se atrasa todo el equipo.

## 2. Roles
| Rol | Integrante | Es dueño de |
|---|---|---|
| A · Datos e indexación | **Julian** | Corpus, cargadores, fragmentación (R0/R1), embeddings, índice, embeddings de la parte B |
| B · Recuperación y generación | Compañero/a 1 | Recuperación (R2), prompt, cliente del LLM, C0, ejecutor de corridas, LLM de la parte B |
| C · Evaluación e informe | Compañero/a 2 | Caso, preguntas, hipótesis, rúbrica, calificación, métricas, informe |

Los compañeros figuran como "Compañero/a 1/2" hasta saber sus nombres.

## 3. Contratos entre componentes (acordar hoy)
Julian define el formato de fragmento porque lo produce él; B y C pueden empezar con fragmentos de prueba con este formato.

```python
# Fragmento (A → B)
{"chunk_id": "manual_vpn.pdf::p3::c2", "archivo": "manual_vpn.pdf", "formato": "pdf",
 "localizador": "p. 3",            # página | sección | párrafo | líneas 10-24
 "texto": "...", "n_tokens": 398, "config_fragmentacion": "R0"}

# Interfaz que Julian entrega a B
indexar(carpeta, config) -> indice            # persiste en indices/<config>/
cargar_indice(config) -> (fragmentos, matriz_embeddings, modelo_emb)
embeber_consulta(texto, config) -> vector     # MISMO modelo que el índice

# Resultado de recuperación (B)
[{"chunk_id": "...", "puntaje": 0.82, "rango": 1}, ...]

# Configuración (compartida, en config.py o configs.yaml)
{"nombre": "R0", "chunk_size": 400, "overlap": 60, "unidad": "tokens (<tokenizador>)",
 "k": 4, "tipo_busqueda": "densa", "modelo_embeddings": "<id>", "modelo_llm": "<id>",
 "temperatura": 0, "max_tokens_salida": 512, "max_tokens_contexto": 2400}
```

Registro de corrida (B → C): `plantillas/registro_corridas.csv` para calificar y `corridas.jsonl` para el detalle (contexto enviado y respuesta completa), unidos por `run_id`.

## 4. Tareas por integrante

### A — Julian (datos e indexación)
| # | Tarea | Criterio de terminado | Depende de | Horas | Fecha |
|---|---|---|---|---|---|
| A1 | Reunir el corpus con C: ≥3 archivos con contenido distinto, ≥2 formatos (propuesta: 1 PDF, 2 DOCX, 1–2 MD) | `corpus/` + `corpus/README.md` con origen, licencia o "sintético"; el PDF tiene texto seleccionable | S1 (caso) | 3 | mar 17 |
| A2 | Cargadores PDF (pypdf/pdfplumber), DOCX (python-docx), MD | Cada archivo produce `(texto, localizador)`: página en PDF, encabezado o párrafo en DOCX, encabezado y líneas en MD; se probó a mano que 3 localizadores apuntan al lugar correcto | A1 | 4 | mar 17 |
| A3 | Fragmentador R0: 400 tokens, 60 de solapamiento | Fragmentos con el formato del contrato; el tokenizador está declarado (el del modelo de embeddings) | A2 | 2 | mié 18 |
| A4 | Embeddings + índice con coseno (p. ej. `intfloat/multilingual-e5-small` local, con prefijos `query:`/`passage:`) | `indexar()`/`cargar_indice()`/`embeber_consulta()` funcionan; el ID del modelo queda en la configuración; un índice persistido por configuración | A3 | 3 | mié 18 |
| A5 | Fragmentador R1: **una** regla y declararla (recomendado: 200/30, mantiene el 15 %; alternativa: por sección con un máximo de ~400) | R1 reindexado aparte; la regla escrita en `config.py` y en el informe; ningún fragmento supera el límite del modelo de embeddings (e5 corta en 512) | A3 | 2 | jue 19 |
| A6 | Parte B: segundo modelo de embeddings (p. ej. `BAAI/bge-m3` o `all-MiniLM`) | Índice R0 reconstruido con el modelo nuevo; las consultas se codifican con el mismo modelo nuevo | A4 | 2 | jue 19 |
| A7 | Apoyar a C con la evidencia de las 9 preguntas | Cada pasaje necesario tiene `chunk_id`/archivo/localizador verificados en R0 y R1 | S3 | 2 | jue 19 |
| A8 | Segunda calificación (independiente de C) | Las 54 corridas calificadas por Julian; desacuerdos marcados | Corridas | 3 | sáb 21 |
| A9 | Sección "Ingesta e indexación" del informe + esquema del flujo | Texto y diagrama entregados a C | A5 | 2 | dom 22 |
| | | | | **23** | |

### B — Compañero/a 1 (recuperación y generación)
| # | Tarea | Criterio de terminado | Depende de | Horas | Fecha |
|---|---|---|---|---|---|
| B1 | Cliente del LLM con la clave en una variable de entorno | `.env.example` sin claves, `.env` en `.gitignore`; ID del modelo, temperatura 0 y límite de salida registrados; reintentos con espera | — | 2 | mar 17 |
| B2 | Recuperación densa top-k (k=4) sobre la interfaz de A | `recuperar(consulta, config)` devuelve el resultado del contrato; probado con fragmentos de prueba y luego con el índice real | Contrato, A4 | 2 | mié 18 |
| B3 | Plantilla de prompt RAG: solo con el contexto, cita `[archivo, localizador]`, frase fija de abstención | Una única plantilla para R0–R2 en `prompts/rag.txt` | B1 | 2 | mié 18 |
| B4 | Límite de contexto (2400 tokens) y registro de recortes | Se registran los fragmentos enviados y si hubo recorte | B2 | 1 | mié 18 |
| B5 | **Hito R0 de punta a punta** | 1 pregunta → respuesta con cita correcta | A4, B2–B4 | 1 | mié 18 |
| B6 | R2: k=8 (opcional: híbrida densa + BM25 con RRF y k=4) | Solo cambia eso respecto a R0; con k=8 el límite de 2400 produce recortes visibles | B5 | 2 | jue 19 |
| B7 | C0: mismo LLM sin documentos; pedirle que señale si no sabe; sin citas | Prompt C0 propio en `prompts/c0.txt` | B1 | 1 | jue 19 |
| B8 | Ejecutor de corridas | 9 preguntas × configuración → `corridas.jsonl` + CSV; mide el tiempo; registra y repite los fallos | B5 | 4 | jue 19 |
| B9 | Corridas finales: A (R0, R1, R2, C0 = 36) y B (R0+embeddings nuevos, R0+LLM nuevo = 18) | 54 filas en el registro; parámetros congelados | S4, S5 | 2 | vie 20 |
| B10 | Cuaderno final ejecutable | Dependencias, pasos, corpus incluido, configuraciones identificadas, sin claves ni salidas con claves | Todo | 3 | dom 22 |
| | | | | **20** | |

### C — Compañero/a 2 (evaluación e informe)
| # | Tarea | Criterio de terminado | Depende de | Horas | Fecha |
|---|---|---|---|---|---|
| C1 | Documento del caso de uso | `plantillas/caso_de_uso.md` completo y aprobado por los tres | S1 | 1 | lun 16 |
| C2 | Escribir los documentos sintéticos del corpus con Julian | Contenido distinto por archivo, con hechos que se cruzan para las preguntas multi-documento | S1 | 3 | mar 17 |
| C3 | 9 preguntas de referencia (3 directas, 3 multi-documento, 3 sin respuesta) | Respuesta esperada + evidencia literal con archivo y localizador; las N justificadas y probadas en C0 para descartar que el LLM las sepa | A2 | 4 | jue 19 |
| C4 | Hipótesis R1/R2/C0/B | `plantillas/hipotesis.md` fechado en un commit antes de las corridas | — | 1 | jue 19 |
| C5 | Rúbrica | `plantillas/rubrica_evaluacion.md` con casos dudosos ya decididos | — | 1 | jue 19 |
| C6 | Primera calificación de las 54 corridas | Todas las columnas de valoración llenas | B9 | 4 | sáb 21 |
| C7 | Métricas y tabla de resultados | Cobertura (recuperado/contexto, /6), corrección (/6), respaldo (proporción o «no aplica»), abstención (/3), tiempo | C6, A8 | 2 | sáb 21 |
| C8 | Informe completo | Todas las secciones de `plantillas/informe_estructura.md`, incluida la declaración de uso de IA | C7 | 6 | dom 22 |
| | | | | **22** | |

## 5. Tareas compartidas
| Tarea | Coordinador | Participan | Criterio de terminado | Fecha |
|---|---|---|---|---|
| S1 · Elegir el caso y el corpus | Compañero/a 2 | Todos | Caso escrito y lista de archivos acordada | lun 16 |
| S2 · Acordar los contratos | **Julian** | Compañero/a 1 | Sección 3 de este plan aprobada; `config.py` creado | lun 16 |
| S3 · Revisión de las preguntas | Compañero/a 2 | Julian (evidencia), Compañero/a 1 (prueba en C0) | Las 9 preguntas pasan la checklist de `preguntas_referencia.md` | jue 19 |
| S4 · Congelar preguntas, hipótesis y configuraciones | Compañero/a 2 | Todos | Commit fechado antes de B9 | jue 19 noche |
| S5 · Revisión cruzada de código | Compañero/a 1 | Julian revisa B y B revisa A | Comentarios resueltos | jue 19 |
| S6 · Resolver los desacuerdos de calificación | Compañero/a 2 | Julian | Desacuerdos anotados con su resolución | sáb 21 |
| S7 · Prueba de reproducibilidad | Compañero/a 2 | — | El cuaderno corre desde cero en una máquina limpia | lun 23 a.m. |
| S8 · Ensayo de sustentación | **Julian** | Todos | Cada uno explicó un componente que no hizo | mar 24 |

## 6. Cronograma
| Día | Julian (A) | Compañero/a 1 (B) | Compañero/a 2 (C) | Hito |
|---|---|---|---|---|
| lun 16 | S2 contratos, `config.py`, probar cargadores con 1 archivo | B1 cliente LLM | S1 caso, C1 | Caso + contratos |
| mar 17 | A1 corpus, A2 cargadores | B2/B3 con fragmentos de prueba | C2 documentos sintéticos | Corpus congelado |
| mié 18 | A3, A4 índice R0 | B4, **B5** | C3 borrador de preguntas | **R0 de punta a punta** |
| jue 19 | A5 R1, A6 embeddings B, A7 evidencia | B6, B7, B8 | C3, C4, C5 | **Preguntas + hipótesis congeladas (S4)** |
| vie 20 | Apoyo a B9; arreglos | **B9 corridas finales** (54) | Revisión de los registros | Corridas completas |
| sáb 21 | A8 segunda calificación | Reintentos si faltan corridas | C6, C7 | Métricas |
| dom 22 | A9 sección + esquema | B10 cuaderno | C8 informe | Borrador final |
| lun 23 | Revisión del informe | Ajustes al cuaderno | S7 reproducibilidad | **Entrega 6:00 p.m.** |
| mar 24 | S8 ensayo | S8 | S8 | Ensayo |
| mié 25 | — | — | — | Sustentación |

## 7. Riesgos y decisiones técnicas
| Riesgo / decisión | Qué hacemos | Quién lo vigila |
|---|---|---|
| PDF sin texto seleccionable | Probar la extracción el lun 16 antes de elegir el PDF | Julian |
| Localizadores incorrectos (una página corrida, secciones DOCX sin estilos de encabezado) | Verificar a mano 3 localizadores por formato; en DOCX, usar el estilo Heading o el número de párrafo | Julian |
| Fragmentos que superan el límite del modelo de embeddings | Contar tokens con el tokenizador del modelo; en R1 por sección, aplicar un máximo | Julian |
| Distinto modelo para consultas y documentos | `embeber_consulta()` usa el modelo de la configuración del índice; se valida al cargar | Julian |
| Parte B cambia dos cosas a la vez | Dos experimentos separados (embeddings y LLM), 9 preguntas cada uno | Compañero/a 1 |
| Preguntas "sin respuesta" que el LLM sabe | Corpus sintético; probar las N en C0 antes de congelarlas | Compañero/a 2 |
| Límite de contexto que nunca recorta | 2400 tokens: con k=8 × 400 recorta; registrar `hubo_recorte` | Compañero/a 1 |
| Hipótesis escritas después de ver resultados | Commit fechado (S4) antes de B9 | Compañero/a 2 |
| Límites de uso de OpenRouter o fallos del proveedor | Revisar la cuota el lun 16; reintentos con espera; correr el viernes, no el domingo | Compañero/a 1 |
| Claves filtradas | `.env` en `.gitignore`; limpiar las salidas del cuaderno antes de entregar | Compañero/a 1 |
| Semilla no fijable | Registrarlo como límite de la comparación | Compañero/a 2 |

**Recortes permitidos si hay atraso** (sin perder requisitos): R2 solo k=8 (sin híbrida); R1 por tamaño (sin cortes por sección); 2 DOCX → 1 DOCX.

## 8. Preparación de la sustentación (40 % individual)
| Componente | Lo hizo | Lo explica en el ensayo |
|---|---|---|
| A · Ingesta e indexación | Julian | Compañero/a 2 |
| B · Recuperación y generación | Compañero/a 1 | Julian |
| C · Evaluación y métricas | Compañero/a 2 | Compañero/a 1 |

Julian debe poder explicar además: por qué el mismo modelo de embeddings para consultas y documentos, qué es la similitud coseno, el efecto esperado del tamaño de fragmento (R1), qué pasa con k=8 y el límite de contexto (R2), y cómo se calcula cada métrica.

## 9. Checklist de entrega
- [ ] Cuaderno ejecutable: dependencias, instalación y ejecución, corpus incluido, configuraciones identificadas, credenciales documentadas sin claves
- [ ] Paquete de evaluación: preguntas con referencias + registros de las 54 corridas
- [ ] Informe: caso, esquema del flujo, hipótesis, tabla de resultados, análisis (R1/R2/C0/B), configuración recomendada, declaración de uso de IA
- [ ] Hipótesis con fecha anterior a las corridas
- [ ] Sin archivos de skills ni `.claude/` en el repositorio
