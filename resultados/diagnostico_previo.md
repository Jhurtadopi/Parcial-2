# Diagnóstico Previo — Proyecto RAG

**Fecha:** 2026-11-20  
**Contexto:** Mesa de Ayuda de TI (Instituto Tecnológico Cóndor)  
**Objetivo:** Diagnóstico analítico del comportamiento de recuperación y contexto (R2 y B_EMB) sin llamadas al LLM, y definición de preguntas de desarrollo.

---

## 1. Diagnóstico de R2 ($k=8$): Tokens de Contexto y Recortes

En la configuración **R2**, se amplía la recuperación densa de $k=4$ a $k=8$ fragmentos de tamaño fijo (400 tokens con 60 de solapamiento). El límite máximo de contexto fijado para el LLM es de **2400 tokens**.

### Resultado General
- **¿Hubo recorte?** **SÍ, en el 100% de las preguntas (9 de 9).**
- **Causa técnica:** Cada fragmento de 400 tokens, sumado a su encabezado de metadatos (`[F#] (archivo · localizador)`), ocupa en promedio entre 320 y 380 tokens. Ocho fragmentos acumulan entre 2400 y 2872 tokens, superando la ventana de contexto de 2400 tokens. La función `construir_contexto()` corta de manera preventiva en el primer fragmento que excede el cupo acumulado.

### Detalle por Pregunta

| Pregunta | Tipo | Tokens Usados | Tokens Recuperados | Recorte | Cantidad Recortados | Fragmentos Recortados (Rango, Chunk ID y Score) |
|---|---|:---:|:---:|:---:|:---:|---|
| **D1** | Directa | 2.330 | 2.801 | **SÍ** | 1 | **R8:** `faq_mesa_ayuda.md::c1` (score: 0.841) |
| **D2** | Directa | 1.980 | 2.403 | **SÍ** | 3 | **R6:** `manual_conectividad_vpn.pdf::c3` (0.845)<br>**R7:** `faq_mesa_ayuda.md::c1` (0.844)<br>**R8:** `catalogo_servicios_sla.docx::c1` (0.844) |
| **D3** | Directa | 1.954 | 2.413 | **SÍ** | 3 | **R6:** `procedimiento_incidentes_seguridad.docx::c2` (0.828)<br>**R7:** `faq_mesa_ayuda.md::c1` (0.826)<br>**R8:** `politica_cuentas_contrasenas.docx::c3` (0.826) |
| **M1** | Multidocumento | 2.045 | 2.424 | **SÍ** | 3 | **R6:** `procedimiento_incidentes_seguridad.docx::c3` (0.861)<br>**R7:** `faq_mesa_ayuda.md::c2` (0.856)<br>**R8:** `procedimiento_incidentes_seguridad.docx::c2` (0.854) |
| **M2** | Multidocumento | 2.220 | 2.495 | **SÍ** | 3 | **R6:** `manual_conectividad_vpn.pdf::c4` (0.842)<br>**R7:** `catalogo_servicios_sla.docx::c3` (0.836)<br>**R8:** `catalogo_servicios_sla.docx::c2` (0.836) |
| **M3** | Multidocumento | 2.363 | 2.546 | **SÍ** | 3 | **R6:** `politica_cuentas_contrasenas.docx::c3` (0.855)<br>**R7:** `politica_cuentas_contrasenas.docx::c2` (0.855)<br>**R8:** `faq_mesa_ayuda.md::c2` (0.853) |
| **N1** | Sin respuesta | 2.189 | 2.648 | **SÍ** | 3 | **R6:** `procedimiento_incidentes_seguridad.docx::c2` (0.830)<br>**R7:** `catalogo_servicios_sla.docx::c3` (0.829)<br>**R8:** `politica_cuentas_contrasenas.docx::c1` (0.828) |
| **N2** | Sin respuesta | 2.391 | 2.872 | **SÍ** | 2 | **R7:** `politica_cuentas_contrasenas.docx::c1` (0.844)<br>**R8:** `manual_conectividad_vpn.pdf::c4` (0.842) |
| **N3** | Sin respuesta | 2.342 | 2.825 | **SÍ** | 2 | **R7:** `politica_cuentas_contrasenas.docx::c2` (0.816)<br>**R8:** `procedimiento_incidentes_seguridad.docx::c3` (0.813) |

> **Conclusión para sustentación (R2):** R2 demuestra con éxito la hipótesis técnica: ampliar $k=8$ permite capturar fragmentos marginales, pero el límite de 2400 tokens opera como un filtro estricto, dejando por fuera sistemáticamente entre 1 y 3 fragmentos (los de menor similitud del top-8). A pesar del recorte, en las 6 preguntas respondibles toda la evidencia esencial estuvo en los primeros rangos (1 a 5), por lo que la cobertura de contexto se mantuvo en 6/6.

---

## 2. Diagnóstico de B_EMB (`BAAI/bge-m3`): Falla de Cobertura en M1, M2 y M3

En el experimento **B_EMB**, se sustituye el modelo de embeddings `multilingual-e5-small` (384 dimensiones) por `BAAI/bge-m3` (1024 dimensiones) manteniendo $k=4$. La cobertura de evidencia en preguntas multidocumento cayó a **0/3** (falla en M1, M2 y M3).

### Análisis Detallado por Pregunta

#### Caso M1: Cuenta bloqueada (Prioridad + SLA)
- **Consulta:** *"Mi cuenta quedó bloqueada y no puedo trabajar. ¿Qué prioridad tiene mi caso y en cuánto tiempo me deben dar la primera respuesta y resolverlo?"*
- **Evidencias requeridas:**
  1. `faq_mesa_ayuda.md::c1` (Clasificación: Cuenta bloqueada $\rightarrow$ P2).
  2. `catalogo_servicios_sla.docx::c2` (SLA: P2 primera respuesta 1 hora, resolución 8 horas).
- **Ranking B_EMB:**
  - Rango 1: `catalogo_servicios_sla.docx::c2` (score: **0.5541**) $\rightarrow$ **Recuperado (Evidencia 2 adentro)**.
  - Rango 2: `politica_cuentas_contrasenas.docx::c2` (score: **0.5441**).
  - Rango 3: `procedimiento_incidentes_seguridad.docx::c3` (score: **0.5178**).
  - Rango 4: `politica_cuentas_contrasenas.docx::c3` (score: **0.4971**).
  - *Rango 7:* `faq_mesa_ayuda.md::c1` (score: **0.4711**) $\rightarrow$ ❌ **PERDIDO (Rango $7 > 4$)**.
- **Por qué falla:** La pregunta menciona "cuenta bloqueada", lo que atrajo con fuerza fragmentos de la *Política de contraseñas* y del documento distractor de *Procedimiento de incidentes*. Estos fragmentos superaron a la tabla de incidentes de la FAQ (`c1`), dejándola en el puesto 7. Al faltar la prioridad P2, la cobertura es 0.

#### Caso M2: Error VPN E-509 (Significado + Solución + Requisito CóndorAuth)
- **Consulta:** *"La VPN me muestra el error E-509. ¿Qué significa, cómo lo soluciono y qué necesito para poder hacerlo?"*
- **Evidencias requeridas:**
  1. `manual_conectividad_vpn.pdf::c3` (E-509 = Certificado vencido, renovar en autoservicio).
  2. `politica_cuentas_contrasenas.docx::c2` (Autoservicio exige aprobación en CóndorAuth; si cambió teléfono, presencial en mesa de ayuda).
- **Ranking B_EMB:**
  - Rango 1: `manual_conectividad_vpn.pdf::c3` (score: **0.6802**) $\rightarrow$ **Recuperado (Evidencia 1 adentro)**.
  - Rango 2: `manual_conectividad_vpn.pdf::c2` (score: **0.5344**).
  - Rango 3: `manual_conectividad_vpn.pdf::c4` (score: **0.5049**).
  - Rango 4: `manual_conectividad_vpn.pdf::c1` (score: **0.4868**).
  - *Rango 5:* `politica_cuentas_contrasenas.docx::c2` (score: **0.4802**) $\rightarrow$ ❌ **PERDIDO (Rango $5 > 4$)**.
- **Por qué falla (Efecto Monopolio Temático):** `bge-m3` le asignó un peso léxico y contextual tan dominante al término "VPN" que **los 4 primeros puestos del ranking fueron copados por los 4 fragmentos del manual de VPN**. El fragmento de la política de contraseñas (`c2`) quedó en el rango 5 por una diferencia ínfima de **0.0066** frente al rango 4 (`c1`). Al recuperarse solo el manual, falta el requisito de MFA/CóndorAuth.

#### Caso M3: Pérdida de portátil en fin de semana (Prioridad + Canal de guardia + Tiempos)
- **Consulta:** *"Perdí mi portátil institucional un sábado a las 3 de la tarde. ¿Qué prioridad tiene, por qué canal lo reporto a esa hora y en cuánto tiempo me deben responder?"*
- **Evidencias requeridas:**
  1. `faq_mesa_ayuda.md::c1` (Pérdida de portátil = P1).
  2. `catalogo_servicios_sla.docx::c1` (Línea de guardia ext 5000 fuera de horario).
  3. `catalogo_servicios_sla.docx::c1` / `c2` (P1 respuesta en 15 minutos).
- **Ranking B_EMB:**
  - Rango 1: `procedimiento_incidentes_seguridad.docx::c2` (score: **0.5913**).
  - Rango 2: `catalogo_servicios_sla.docx::c2` (score: **0.5704**) $\rightarrow$ **Recuperado (Evidencia 3 adentro)**.
  - Rango 3: `catalogo_servicios_sla.docx::c1` (score: **0.5639**) $\rightarrow$ **Recuperado (Evidencia 2 adentro)**.
  - Rango 4: `procedimiento_incidentes_seguridad.docx::c3` (score: **0.5552**).
  - *Rango 5:* `faq_mesa_ayuda.md::c1` (score: **0.5507**) $\rightarrow$ ❌ **PERDIDO (Rango $5 > 4$)**.
- **Por qué falla:** Los términos "perdí portátil" activaron una fuerte afinidad semántica en `bge-m3` hacia los fragmentos del documento distractor de *Procedimiento de incidentes de seguridad* (`c2` y `c3`), que tratan sobre "pérdida de activos" y "controles de equipos". Esto empujó a `faq_mesa_ayuda.md::c1` al rango 5, quedando fuera por apenas **0.0045** puntos.

---

## 3. Banco de Preguntas de Desarrollo (`evaluacion/preguntas_desarrollo.json`)

Se crearon 4 preguntas completamente nuevas, no presentes en el benchmark congelado, verificadas contra el texto literal del corpus:

1. **DEV_D1 (Directa):** Cuota mensual de páginas blanco y negro y penalización de color.
   - *Evidencia:* `guia_equipos_impresion_software.md` (§ Impresión, líneas 32-34).
2. **DEV_D2 (Directa):** Servicios institucionales que requieren obligatoriamente VPN desde fuera del campus.
   - *Evidencia:* `manual_conectividad_vpn.pdf` (p. 1).
3. **DEV_M1 (Multidocumento):** Instalación de software especializado (requisitos, aprobación, prioridad P4 y tiempo SLA).
   - *Evidencias cruzadas:* `faq_mesa_ayuda.md` (§ Equipos y software) + `catalogo_servicios_sla.docx` (§ 6 y § 4).
4. **DEV_N1 (Sin respuesta):** Costo o tarifa de duplicado físico del carné institucional.
   - *Justificación:* El corpus no contiene costos ni tarifas para reposición física de carné; el modelo debe abstenerse.

