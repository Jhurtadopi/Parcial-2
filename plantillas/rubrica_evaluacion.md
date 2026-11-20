# Rúbrica de evaluación

Calificar cada corrida por separado (evaluador 1 y evaluador 2) y luego resolver los desacuerdos. Anotar cada desacuerdo y su resolución.

## Cobertura de evidencia (solo RAG, preguntas respondibles)
- `cobertura_recuperado = 1` si **todos** los pasajes necesarios (según `preguntas_referencia.md`) aparecen en algún fragmento recuperado.
- `cobertura_contexto = 1` si además siguen en el contexto enviado al LLM después del recorte.
- Reportar: X/6 y Y/6 por variante.

## Corrección (todas las configuraciones, preguntas respondibles)
- `correcta = 1` solo si la respuesta es **correcta y completa** frente a la referencia.
- Una respuesta parcial, una abstención o un error de hecho = 0.
- Reportar: X/6 por configuración.

## Respaldo de las citas (solo RAG)
- `sustantiva = 1` si la respuesta aporta al menos una afirmación que intenta contestar (también en las preguntas sin respuesta).
- Afirmación central: la que contesta directamente lo preguntado (no el contexto ni las cortesías).
- `citas_respaldan = 1` si **todas** las afirmaciones centrales están respaldadas por los pasajes **efectivamente citados**.
- Reportar: (Σ citas_respaldan) / (Σ sustantiva); si el denominador es 0, «no aplica».

## Abstención apropiada (todas, preguntas sin respuesta)
- `abstencion_apropiada = 1` si reconoce que no puede responder **y** no añade una respuesta sin respaldo.
- "No está en los documentos, pero probablemente es X" = 0.
- Reportar: X/3 por configuración.

## Nota sobre C0
C0 usa otro prompt (sin documentos), y en C0 no se evalúan las citas ni la cobertura.
