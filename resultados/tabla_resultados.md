# Tabla de Resultados del Sistema RAG

> **Nota sobre el modelo (desviación del plan):** El modelo base previsto,
> `google/gemma-4-31b-it:free`, estuvo indisponible de forma persistente (HTTP 429,
> saturación del pool gratuito de Google AI Studio en OpenRouter). Las configuraciones
> R0, R1, R2, C0 y B_EMB se ejecutaron con `nvidia/nemotron-3.5-lightning:free` como
> LLM base; B_LLM mantiene su LLM alternativo `nvidia/nemotron-3-ultra-550b-a55b:free`.
> El resto de parámetros (fragmentación, k, embeddings, temperatura 0, semilla 42,
> 512 de salida, 2400 de contexto, razonamiento off) no se modificó. Las hipótesis
> (congeladas) se escribieron asumiendo Gemma; el análisis lo tiene en cuenta.

> **Calificación:** las 9 corridas de B_LLM fueron calificadas previamente; las 45
> corridas de R0/R1/R2/C0/B_EMB llevan una calificación asistida (borrador en
> `evaluacion/valoracion_e2_borrador.csv`) consolidada en `evaluacion/valoracion_final.csv`,
> pendiente de revisión humana final según la rúbrica (doble evaluación).

## 1. Métricas Agregadas por Configuración

| Configuración | Experimento | Cobertura recuperado (/6) | Cobertura contexto (/6) | Corrección (/6) | Respaldo de citas | Abstención apropiada (/3) | Recortes de contexto | Tiempo medio (s) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **R0 (Base)** | A | 5/6 | 5/6 | 5/6 | 83% (5/6) | 2/3 | 0 | 1.16 s |
| **R1 (Ch. 200)** | A | 4/6 | 4/6 | 5/6 | 67% (4/6) | 3/3 | 0 | 0.68 s |
| **R2 (k=8)** | A | 5/6 | 5/6 | 5/6 | 67% (4/6) | 3/3 | 9 | 0.80 s |
| **C0 (Sin RAG)** | A | — | — | 0/6 | — (C0 sin citas) | 3/3 | — | 1.00 s |
| **B_EMB (BGE-M3)** | B | 3/6 | 3/6 | 4/6 | 40% (2/5) | 3/3 | 0 | 0.97 s |
| **B_LLM (Nemotron-Ultra)** | B | 5/6 | 5/6 | 6/6 | 100% (6/6) | 3/3 | 0 | 3.31 s |

---

## 2. Matriz Pregunta × Configuración (Corrección y Abstención)

Convenciones:
- ✔ : respuesta correcta y completa (`correcta = 1`) o abstención apropiada (`abstencion_apropiada = 1`).
- ✘ : incorrecta, incompleta, alucinada, o abstención indebida (`0`).

| ID | Tipo | Tema | R0 | R1 | R2 | C0 | B_EMB | B_LLM |
|:---:|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **D1** | Directa | Dispositivos simultáneos VPN | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ |
| **D2** | Directa | Intentos de bloqueo y duración | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ |
| **D3** | Directa | Tamaño máximo de adjuntos | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ |
| **M1** | Multidoc. | Cuenta bloqueada: prioridad y SLA | ✔ | ✔ | ✔ | ✘ | ✘ | ✔ |
| **M2** | Multidoc. | Error E-509: significado, solución y MFA | ✘ | ✘ | ✘ | ✘ | ✘ | ✔ |
| **M3** | Multidoc. | Portátil perdido: prioridad, canal y SLA | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ |
| **N1** | Sin resp. | Presupuesto anual | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| **N2** | Sin resp. | Retención de logs VPN | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| **N3** | Sin resp. | Sanción por compartir contraseña | ✘ | ✔ | ✔ | ✔ | ✔ | ✔ |

---

## 3. Lectura de los resultados (para el análisis del informe)

- **C0 vs R0 (valor del RAG):** C0 acierta **0/6** en las respondibles porque la institución
  es ficticia y el modelo no la conoce de memoria; se abstiene en todo. R0, con los
  documentos, acierta **5/6**. Es la evidencia más clara del aporte del RAG.
- **R1 vs R0 (fragmentación):** la cobertura recuperada baja de 5/6 a 4/6; con fragmentos de
  200 tokens el pasaje multidocumento se parte. La corrección se mantiene 5/6 por coincidencia
  (M3 sigue acertando pese a la menor cobertura). Confirma parcialmente la hipótesis.
- **R2 vs R0 (k=8):** recorte de contexto en **las 9 preguntas** (el único con recortes), sin
  ganar cobertura frente a R0. Confirma la hipótesis: ampliar k choca con el límite de 2400
  tokens y no mejora la evidencia útil. El respaldo de citas baja (67 %) por más texto distractor.
- **B_EMB vs R0 (embeddings):** la cobertura cae a **3/6** y las multidocumento se degradan
  (M1 falla), confirmando el "efecto monopolio temático" de bge-m3 descrito en el diagnóstico.
- **B_LLM vs R0 (LLM):** con la misma recuperación, el LLM alternativo (Nemotron-Ultra) logra
  **6/6** y respaldo 100 %, incluso en M2, donde los modelos sobre lightning fallan. Diferencia
  de seguimiento de instrucciones entre modelos.
- **M2 es la pregunta difícil:** falla en todas las variantes densas (R0, R1, R2, B_EMB) porque
  la evidencia del requisito de MFA/CóndorAuth no llega al contexto; solo B_LLM la resuelve.
- **N3 (alucinación):** R0 inventó "sanción administrativa según el Reglamento Interno" en vez
  de abstenerse (abstención 2/3). Las demás variantes se abstuvieron correctamente.

> Los números provienen de `resultados/tabla_resultados.csv`, calculado con la función
> `calcular_metricas()` del cuaderno sobre `evaluacion/valoracion_final.csv`.
