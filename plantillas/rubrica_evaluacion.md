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

---

## Casos dudosos y decisión

Guía de criterio uniforme para evaluar corridas ambiguas o limítrofes entre los dos evaluadores:

### 1. Respuesta correcta citando el fragmento equivocado
- **Situación:** La respuesta acierta el dato fáctico frente a la referencia, pero cita un fragmento que no contiene dicha afirmación (p. ej., responde "3 dispositivos simultáneos" citando `[F3]`, cuando la evidencia real estaba en `[F1]`).
- **Decisión:** `correcta = 1`, `sustantiva = 1`, `citas_respaldan = 0`, `abstencion_apropiada = —`.
- **Criterio:** La corrección evalúa la veracidad frente a la referencia; el respaldo evalúa estrictamente que los fragmentos **efectivamente citados** demuestren lo afirmado. Si el fragmento citado no contiene la evidencia, no hay respaldo documental.

### 2. Abstención con dato adicional o conjetura ("abstención contaminada")
- **Situación:** En una pregunta sin respuesta (N), el modelo emite la frase de abstención pero añade una estimación o conocimiento externo (p. ej., *"EVIDENCIA INSUFICIENTE: no se indica el presupuesto, pero en universidades suele rondar el 5 %"*).
- **Decisión:** `correcta = —`, `sustantiva = 1`, `citas_respaldan = 0`, `abstencion_apropiada = 0`.
- **Criterio:** La regla de abstención apropiada exige reconocer que no puede responder **y no añadir una respuesta sin respaldo**. Al especular o dar datos no fundamentados, la abstención queda invalidada.

### 3. Cita a una etiqueta de fragmento inexistente en el contexto (p. ej., `[F9]`)
- **Situación:** La respuesta fáctica es correcta, pero el modelo alucina una etiqueta numérica que no forma parte del contexto enviado (p. ej., en R0 con $k=4$ cita `[F8]` o `[F9]`).
- **Decisión:** `correcta = 1`, `sustantiva = 1`, `citas_respaldan = 0`, `abstencion_apropiada = —`.
- **Criterio:** Citar un identificador inexistente es una alucinación formal. No es posible validar el respaldo sobre una fuente que nunca fue provista en el prompt.

### 4. Falsa abstención en pregunta respondible (`EVIDENCIA INSUFICIENTE` en D o M)
- **Situación:** El modelo declara no tener información suficiente ante una pregunta directa o multidocumento, a pesar de que los fragmentos de contexto contienen la evidencia.
- **Decisión:** `correcta = 0`, `sustantiva = 0`, `citas_respaldan = —` (no aplica), `abstencion_apropiada = —`.
- **Criterio:** Una abstención en una pregunta respondible cuenta estrictamente como incorrecta (`correcta = 0`). Al no ser sustantiva, queda excluida del denominador de respaldo de citas.

### 5. Configuración C0 (sin RAG) que acierta por conocimiento general preentrenado
- **Situación:** En C0, el LLM responde a una pregunta directa coincidiendo de forma correcta y completa con la referencia por conocimiento previo o coincidencia técnica.
- **Decisión:** `correcta = 1`, `sustantiva = 1`, `citas_respaldan = —` (no aplica en C0), `abstencion_apropiada = —`.
- **Criterio:** En C0 se mide la capacidad del modelo base sin RAG. Si la respuesta es exacta y completa es `correcta = 1`. En C0 las citas nunca se evalúan ni computan.

### 6. Respuesta correcta pero incompleta en pregunta multidocumento
- **Situación:** En M1 (pide prioridad y tiempos SLA de respuesta y resolución), el modelo responde únicamente la prioridad (P2), omitiendo los tiempos comprometidos de 1 hora y 8 horas.
- **Decisión:** `correcta = 0`, `sustantiva = 1`, `citas_respaldan = 1` (si la prioridad P2 citada está respaldada en su fragmento), `abstencion_apropiada = —`.
- **Criterio:** La definición de corrección exige que la respuesta sea **correcta y completa**. Las respuestas parciales son calificadas con 0. Sin embargo, la afirmación emitida sí es sustantiva y puede tener respaldo documental válido en sus citas.

### 7. Respuesta correcta con citas válidas, pero que añade una afirmación secundaria no respaldada
- **Situación:** Responde correctamente lo preguntado citando bien su fragmento, pero agrega una afirmación accesoria inventada (p. ej., en D3 cita los 25 MB en `[F2]`, pero agrega que *"los correos se eliminan cada 6 meses"* sin respaldo).
- **Decisión:** `correcta = 0`, `sustantiva = 1`, `citas_respaldan = 0`, `abstencion_apropiada = —`.
- **Criterio:** Añadir información falsa o no verificable en el corpus invalida la corrección completa. Además, la regla de respaldo exige que **todas** las afirmaciones sustantivas emitidas estén sustentadas por los pasajes citados.

### 8. Respuesta correcta omitiendo por completo las citas entre corchetes
- **Situación:** En una configuración RAG (R0, R1, R2, B_EMB o B_LLM), el modelo responde de forma fáctica perfecta frente a la referencia, pero olvida incluir los corchetes de citación (p. ej., no escribe `[F1]`).
- **Decisión:** `correcta = 1`, `sustantiva = 1`, `citas_respaldan = 0`, `abstencion_apropiada = —`.
- **Criterio:** El contenido es verídico y responde lo solicitado, pero no cumple con el contrato de trazabilidad documental. Al no existir citas, no hay respaldo verificable.

### 9. Pregunta sin respuesta (N) donde el modelo alucina una respuesta sustantiva
- **Situación:** En N2 (retención de logs de VPN, ausente en el corpus), el modelo inventa un plazo verosímil y cita un fragmento (p. ej., *"Los logs se conservan por 6 meses [F2]"*).
- **Decisión:** `correcta = —`, `sustantiva = 1`, `citas_respaldan = 0`, `abstencion_apropiada = 0`.
- **Criterio:** Falla doblemente: inventa información inexistente (alucinación factual) y cita un fragmento que no contiene tal dato, violando la instrucción de abstenerse.
