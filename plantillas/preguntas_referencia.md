# Preguntas de referencia (congeladas el 2026-11-21)

> No modificar después de iniciar las corridas finales.

| ID | Tipo | Pregunta | Respuesta esperada | Evidencia necesaria (archivo · localizador) |
|---|---|---|---|---|
| D1 | Directa | ¿Cuántos dispositivos puede tener conectados al mismo tiempo un usuario a la VPN? | Como máximo 3 dispositivos conectados a la VPN de forma simultánea. | manual_conectividad_vpn.pdf · p. 2 |
| D2 | Directa | ¿Después de cuántos intentos fallidos se bloquea una cuenta institucional y cuánto dura el bloqueo automático? | Se bloquea tras 5 intentos fallidos en un período de 15 minutos, y el bloqueo automático se levanta solo después de 30 minutos. | politica_cuentas_contrasenas.docx · § 4. Bloqueo y desbloqueo de cuentas, párr. 1; politica_cuentas_contrasenas.docx · § 4. Bloqueo y desbloqueo de cuentas, párr. 2 |
| D3 | Directa | ¿Cuál es el tamaño máximo de los archivos adjuntos en el correo institucional? | Como máximo 25 MB en adjuntos por mensaje, tanto al enviar como al recibir. | faq_mesa_ayuda.md · § Correo y almacenamiento, líneas 46-48 |
| M1 | Multi-documento | Mi cuenta quedó bloqueada y no puedo trabajar. ¿Qué prioridad tiene mi caso y en cuánto tiempo me deben dar la primera respuesta y resolverlo? | Prioridad P2 (FAQ). Para P2 la primera respuesta es en 1 hora hábil y la resolución objetivo en 8 horas hábiles (catálogo de servicios). | faq_mesa_ayuda.md · § Clasificación de incidentes comunes, líneas 22-31; catalogo_servicios_sla.docx · § 4. Tiempos de respuesta y de resolución, párr. 2 |
| M2 | Multi-documento | La VPN me muestra el error E-509. ¿Qué significa, cómo lo soluciono y qué necesito para poder hacerlo? | Es un certificado de dispositivo vencido (vigencia de 365 días). Se soluciona ingresando al portal de autoservicio (autoservicio.itc.example), opción Dispositivos > Renovar certificado, y luego reiniciando el cliente CóndorVPN. Para hacerlo se exige una aprobación en CóndorAuth; si el usuario cambió de teléfono o perdió el dispositivo con CóndorAuth, debe presentarse en la mesa de ayuda con su documento de identidad para reiniciar el enrolamiento de MFA. | manual_conectividad_vpn.pdf · p. 3; politica_cuentas_contrasenas.docx · § 3. Autenticación de dos factores (MFA), párr. 2; politica_cuentas_contrasenas.docx · § 3. Autenticación de dos factores (MFA), párr. 3 |
| M3 | Multi-documento | Perdí mi portátil institucional un sábado a las 3 de la tarde. ¿Qué prioridad tiene, por qué canal lo reporto a esa hora y en cuánto tiempo me deben responder? | Es prioridad P1. A esa hora la mesa de ayuda está cerrada (horario de sábados de 8:00 a 12:00), por lo que se reporta a través de la línea de guardia en la extensión 5000 o al número externo 601-555-5000; la primera respuesta para P1 es en 15 minutos, en cualquier día y hora (24x7). | faq_mesa_ayuda.md · § Clasificación de incidentes comunes, líneas 22-31; catalogo_servicios_sla.docx · § 2. Canales y horario de atención, párr. 1; catalogo_servicios_sla.docx · § 2. Canales y horario de atención, párr. 2; catalogo_servicios_sla.docx · § 4. Tiempos de respuesta y de resolución, párr. 1 |
| N1 | Sin respuesta | ¿Cuál es el presupuesto anual asignado a la mesa de ayuda de TI? | — | — |
| N2 | Sin respuesta | ¿Durante cuánto tiempo se conservan los registros (logs) de las conexiones a la VPN? | — | — |
| N3 | Sin respuesta | ¿Qué sanción recibe un funcionario que comparte su contraseña con otra persona? | — | — |

## Justificación de las preguntas sin respuesta
| ID | Por qué el corpus no permite responderla | ¿Podría el LLM saberla de memoria? (si sí, cambiarla) |
|---|---|---|
| N1 | Ningún documento del corpus menciona presupuestos ni cifras financieras de la mesa. La institución es ficticia, así que el LLM tampoco puede saberlo de memoria. | No. La institución es ficticia (Instituto Tecnológico Cóndor) y el corpus no contiene esta información. |
| N2 | El manual de conectividad habla de límites de sesión y de errores, pero no de retención de registros. Es una pregunta cercana al tema (tienta a responder con la duración de sesiones o con los 30 días de la papelera) pero no tiene respuesta en el corpus. | No. Institución ficticia; tienta a alucinar con la duración de sesiones o papelera (30 días), pero no existe registro de retención de logs. |
| N3 | La política de cuentas define requisitos, bloqueo y desactivación, pero no establece sanciones disciplinarias. Un LLM podría inventar una sanción genérica; la respuesta correcta es abstenerse. | No. Institución ficticia; un modelo podría alucinar una sanción laboral estándar, pero la política institucional no la contempla. |

## Pasajes de evidencia (texto literal)
### D1
> "Cada usuario puede tener como máximo 3 dispositivos conectados a la VPN de forma simultánea. Al intentar conectar un cuarto dispositivo, la sesión más antigua se cierra automáticamente." — manual_conectividad_vpn.pdf, p. 2

### D2
> "Una cuenta se bloquea automáticamente después de 5 intentos de inicio de sesión fallidos en un período de 15 minutos. Cuentan los intentos fallidos en cualquier servicio que use la cuenta institucional, incluida la VPN." — politica_cuentas_contrasenas.docx, § 4. Bloqueo y desbloqueo de cuentas, párr. 1

> "El bloqueo automático se levanta solo después de 30 minutos. Si el usuario necesita el desbloqueo antes, puede pedirlo a la mesa de ayuda, que verificará su identidad con el código de empleado o de estudiante y la fecha de nacimiento registrada." — politica_cuentas_contrasenas.docx, § 4. Bloqueo y desbloqueo de cuentas, párr. 2

### D3
> "Los mensajes pueden tener como máximo 25 MB en adjuntos, tanto al enviar como al recibir. Para archivos más grandes, comparta un enlace de CóndorDrive." — faq_mesa_ayuda.md, § Correo y almacenamiento, líneas 46-48

### M1
> "| Cuenta bloqueada | P2 |" — faq_mesa_ayuda.md, § Clasificación de incidentes comunes, líneas 22-31

> "P2: primera respuesta en 1 hora hábil y resolución objetivo en 8 horas hábiles." — catalogo_servicios_sla.docx, § 4. Tiempos de respuesta y de resolución, párr. 2

### M2
> "E-509 - Certificado de dispositivo vencido. Los certificados de dispositivo tienen una vigencia de 365 días. Para renovarlo, ingrese al portal de autoservicio (autoservicio.itc.example), opción Dispositivos, y pulse Renovar certificado; luego reinicie el cliente CóndorVPN." — manual_conectividad_vpn.pdf, p. 3

> "El portal de autoservicio (autoservicio.itc.example) exige una aprobación en CóndorAuth para cualquier operación sobre la cuenta o sus dispositivos, incluida la renovación de certificados de dispositivo y el cambio de contraseña." — politica_cuentas_contrasenas.docx, § 3. Autenticación de dos factores (MFA), párr. 2

> "Si el usuario cambió de teléfono o perdió el dispositivo con CóndorAuth, no podrá usar el portal de autoservicio. En ese caso debe presentarse en la mesa de ayuda con su documento de identidad para que un técnico reinicie el enrolamiento de MFA. Este trámite no se atiende por teléfono ni por correo." — politica_cuentas_contrasenas.docx, § 3. Autenticación de dos factores (MFA), párr. 3

### M3
> "| Pérdida o robo de un equipo portátil o teléfono con información institucional | P1 |" — faq_mesa_ayuda.md, § Clasificación de incidentes comunes, líneas 22-31

> "La mesa de ayuda atiende de lunes a viernes de 7:00 a 19:00 y los sábados de 8:00 a 12:00, excepto festivos. Los canales son: el portal de soporte (soporte.itc.example), el correo mesadeayuda@itc.example, la extensión telefónica 4000 y la atención presencial en el edificio B, oficina 104." — catalogo_servicios_sla.docx, § 2. Canales y horario de atención, párr. 1

> "Fuera de ese horario solo se atienden casos de prioridad P1, a través de la línea de guardia en la extensión 5000 (o el número externo 601-555-5000). Los casos de otras prioridades registrados fuera de horario se atienden al inicio de la siguiente jornada." — catalogo_servicios_sla.docx, § 2. Canales y horario de atención, párr. 2

> "P1: primera respuesta en 15 minutos y resolución objetivo en 4 horas, en cualquier día y hora (24x7)." — catalogo_servicios_sla.docx, § 4. Tiempos de respuesta y de resolución, párr. 1

