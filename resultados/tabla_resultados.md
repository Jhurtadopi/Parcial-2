# Tabla de Resultados del Sistema RAG

## 1. Métricas Agregadas por Configuración

| Configuración | Experimento | Cobertura recuperado (/6) | Cobertura contexto (/6) | Corrección (/6) | Respaldo de citas | Abstención apropiada (/3) | Recortes de contexto | Tiempo medio (s) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **B_LLM** | B | 5/6 | 5/6 | 6/6 | 100% (6/6) | 3/3 | 0 | 3.31 s |
| *R0 (Base)* | A | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* |
| *R1 (Ch. 200)* | A | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* |
| *R2 (k=8)* | A | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* |
| *C0 (Sin RAG)* | A | — | — | *Pendiente (429)* | — (C0 sin citas) | *Pendiente (429)* | — | *Pendiente (429)* |
| *B_EMB (BGE-M3)* | B | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* | *Pendiente (429)* |

> **Nota sobre el estado de ejecución:** Debido a la saturación del pool compartido aguas arriba de Google AI Studio para `google/gemma-4-31b-it:free` (errores HTTP 429 continuos), las corridas de las configuraciones dependientes de Gemma quedaron detenidas preventivamente según las reglas del proyecto. La variante `B_LLM` (`nvidia/nemotron-3-ultra-550b-a55b:free`) completó el 100 % de sus ejecuciones con cero fallos y costo $0.

---

## 2. Matriz Pregunta × Configuración (Corrección y Abstención)

Convenciones:
- ✔ : Respuesta correcta y completa frente a la referencia (`correcta = 1`) o abstención apropiada sin alucinaciones (`abstencion_apropiada = 1`).
- ✘ : Respuesta incorrecta, incompleta o alucinada (`0`).
- ⏳ : Ejecución pendiente por límite de cuota (HTTP 429).

| ID | Tipo de Pregunta | Tema evaluado | B_LLM | R0 (Base) | R1 | R2 | C0 | B_EMB |
|:---:|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **D1** | Directa | ¿Cuántos dispositivos simultáneos en VPN? | ✔ (1/1) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **D2** | Directa | ¿Intentos fallidos de bloqueo y duración? | ✔ (1/1) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **D3** | Directa | ¿Tamaño máximo de adjuntos en correo? | ✔ (1/1) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **M1** | Multidocumento | Cuenta bloqueada: prioridad y tiempos SLA | ✔ (1/1) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **M2** | Multidocumento | Error E-509: significado, solución y requisitos MFA | ✔ (1/1) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **M3** | Multidocumento | Portátil perdido sábado: prioridad, canal y SLA | ✔ (1/1) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **N1** | Sin respuesta | Presupuesto anual de la mesa de ayuda | ✔ (Abstención) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **N2** | Sin respuesta | Retención de logs de conexiones VPN | ✔ (Abstención) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **N3** | Sin respuesta | Sanción por compartir contraseña | ✔ (Abstención) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |

### Resumen de Desempeño B_LLM:
- **Preguntas respondibles (D1–D3, M1–M3):** 6/6 correctas (100 %).
- **Respaldo de citas:** 100 % (6/6 afirmaciones sustantivas plenamente respaldadas por los fragmentos citados).
- **Preguntas sin respuesta (N1–N3):** 3/3 abstenciones apropiadas (100 %) con la frase contractual `EVIDENCIA INSUFICIENTE:`.
- **Recortes de contexto:** 0 (el contexto máximo utilizado fue de 1603 tokens, muy por debajo de los 2400 permitidos).
