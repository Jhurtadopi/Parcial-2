# Caso de uso

- **Nombre del asistente:** Asistente RAG de Mesa de Ayuda de TI (Instituto Tecnológico Cóndor).
- **Usuarios:** Funcionarios, docentes, contratistas y estudiantes del Instituto Tecnológico Cóndor (ITC), así como técnicos de soporte de nivel 1 de la Mesa de Ayuda de TI. Lo utilizan en situaciones cotidianas de soporte técnico cuando requieren resolver dudas sobre procedimientos institucionales, consultar políticas de seguridad de cuentas y contraseñas, diagnosticar errores de conexión a la VPN o validar los acuerdos de nivel de servicio (SLA) y canales de reporte ante incidencias.
- **Preguntas que debe resolver (en alcance):**
  1. ¿Cuáles son las políticas y requisitos de contraseñas institucionales (longitud mínima, vigencia y aviso previo de vencimiento)?
  2. ¿Cuántos dispositivos simultáneos se permiten en la red VPN (CóndorVPN) y qué ocurre si se intenta conectar un dispositivo adicional?
  3. ¿Bajo qué condiciones se bloquea automáticamente una cuenta de usuario y cuánto tiempo debe esperarse para su desbloqueo automático?
  4. ¿Qué prioridad tiene el reporte de pérdida o robo de un equipo portátil institucional, por qué canal se reporta fuera de horario y cuál es el tiempo de respuesta garantizado por el SLA?
  5. ¿Qué significa el código de error E-509 en CóndorVPN, cómo se soluciona en el portal de autoservicio y qué método de autenticación en dos factores (MFA) se requiere?
- **Fuera de alcance:**
  - Consultas sobre presupuestos, costos financieros, cobros de servicios o tarifas de reposición física de carnés (no existen datos en el corpus).
  - Consultas sobre retención de registros de auditoría (*logs*) de conexiones a la VPN o peritajes forenses (no contemplados en la documentación).
  - Gestión disciplinaria, sanciones laborales o penales por préstamo o uso indebido de contraseñas institucionales (la documentación solo establece controles técnicos).
  - Ejecución transaccional automática de acciones (p. ej., restablecer contraseñas en Active Directory, asignar licencias o desbloquear cuentas de forma directa en bases de datos). El asistente es estrictamente de consulta informativa documental.
  - Trámites académicos, matrículas, nómina o temas administrativos ajenos a la infraestructura y soporte de tecnologías de la información.
- **Comportamiento esperado ante falta de evidencia:** Se abstiene e indica qué información falta (responde exactamente con el prefijo `EVIDENCIA INSUFICIENTE:` seguido de una breve explicación de lo que no figura en los documentos, sin inventar datos).

## Corpus

| Archivo | Formato | Contenido | Origen / licencia | ¿Sintético? | Localizador usado |
|---|---|---|---|---|---|
| `manual_conectividad_vpn.pdf` | PDF (texto seleccionable) | Manual de conectividad remota: requisitos previos, instalación de CóndorVPN, límites de conexión simultánea, códigos de error (E-401, E-403, E-412, E-509, E-610) y redes inalámbricas del campus. | Generado por `herramientas/generar_corpus.py` para el proyecto académico RAG | Sí (sintético) | página (`p. X`) |
| `politica_cuentas_contrasenas.docx` | DOCX | Política de cuentas institucionales: longitud y caducidad de contraseñas, autenticación de dos factores (CóndorAuth), bloqueo automático y cuentas de contratistas. | Generado por `herramientas/generar_corpus.py` para el proyecto académico RAG | Sí (sintético) | sección y párrafo (`§ X, párr. Y`) |
| `catalogo_servicios_sla.docx` | DOCX | Catálogo de servicios y acuerdos de nivel de servicio: canales y horarios de atención, línea de guardia, niveles de prioridad (P1 a P4), tiempos de respuesta/resolución y escalamiento. | Generado por `herramientas/generar_corpus.py` para el proyecto académico RAG | Sí (sintético) | sección y párrafo (`§ X, párr. Y`) |
| `faq_mesa_ayuda.md` | MD | Preguntas frecuentes: canales de soporte, tabla de clasificación de incidentes comunes (P1 a P4), cuotas de correo y CóndorDrive, equipos y reporte de pérdida de portátiles. | Generado por `herramientas/generar_corpus.py` para el proyecto académico RAG | Sí (sintético) | sección y líneas (`§ X, líneas Y-Z`) |
| `procedimiento_incidentes_seguridad.docx` | DOCX | Procedimiento de gestión de incidentes de seguridad de la información, clasificación de datos y controles en equipos (documento distractor con vocabulario afín). | Generado por `herramientas/generar_corpus.py` para el proyecto académico RAG | Sí (sintético) | sección y párrafo (`§ X, párr. Y`) |
| `guia_equipos_impresion_software.md` | MD | Guía de uso de equipos institucionales, cuotas de impresión mensual, multifuncionales y catálogo de software disponible (documento distractor con vocabulario afín). | Generado por `herramientas/generar_corpus.py` para el proyecto académico RAG | Sí (sintético) | sección y líneas (`§ X, líneas Y-Z`) |

Datos aptos para procesamiento por servicios externos: Sí (corpus sintético)
