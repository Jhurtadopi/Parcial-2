"""Genera el corpus SINTÉTICO del proyecto RAG (mesa de ayuda de TI ficticia).

Todo el contenido es inventado: describe una institución ficticia, el
"Instituto Tecnológico Cóndor" (ITC), y usa dominios reservados *.example.
No contiene datos reales ni personales, así que se puede enviar a servicios
externos (OpenRouter).

Archivos generados en corpus/:
  - manual_conectividad_vpn.pdf          (PDF con texto seleccionable, localizador: página)
  - politica_cuentas_contrasenas.docx    (DOCX con encabezados, localizador: sección y párrafo)
  - catalogo_servicios_sla.docx          (DOCX con encabezados, localizador: sección y párrafo)
  - faq_mesa_ayuda.md                    (Markdown, localizador: sección y líneas)
  - procedimiento_incidentes_seguridad.docx  (DOCX, documento distractor)
  - guia_equipos_impresion_software.md       (Markdown, documento distractor)

Los dos documentos "distractores" comparten vocabulario con los demás pero no
responden las preguntas de evaluación; así la recuperación no es trivial.

Uso:  python herramientas/generar_corpus.py
Requiere: fpdf2, python-docx
"""
from pathlib import Path

from docx import Document
from fpdf import FPDF

RAIZ = Path(__file__).resolve().parent.parent
CORPUS = RAIZ / "corpus"
AVISO = ("DOCUMENTO SINTÉTICO - Contenido ficticio creado para el proyecto académico RAG "
         "de Sistemas Inteligentes. El Instituto Tecnológico Cóndor no existe.")

# ---------------------------------------------------------------------------
# 1. PDF: Manual de conectividad (VPN y Wi-Fi). Cada lista es una página.
# ---------------------------------------------------------------------------
MANUAL_VPN = [
    ("Manual de conectividad remota y redes inalámbricas", [
        AVISO,
        "Versión 3.2 - Mesa de Ayuda de TI del Instituto Tecnológico Cóndor (ITC).",
        "1. Propósito",
        "Este manual explica cómo conectarse a los servicios internos del ITC desde fuera del "
        "campus mediante la red privada virtual (VPN) y cómo usar las redes inalámbricas del "
        "campus. Está dirigido a funcionarios, docentes y contratistas con cuenta institucional "
        "activa. Los estudiantes no tienen acceso a la VPN; deben usar los servicios publicados "
        "en el portal web, que no requieren VPN.",
        "2. Servicios que requieren VPN",
        "La VPN es obligatoria para acceder al sistema financiero, al repositorio de documentos "
        "administrativos, a las carpetas compartidas departamentales y a los servidores de "
        "laboratorio. El correo institucional y CóndorDrive funcionan sin VPN.",
        "3. Requisitos previos",
        "Para usar la VPN se necesita: una cuenta institucional activa, la autenticación de dos "
        "factores (MFA) enrolada en la aplicación CóndorAuth, un certificado de dispositivo vigente "
        "y el cliente oficial CóndorVPN instalado. El cliente CóndorVPN está disponible para "
        "Windows 10 y 11, macOS 13 o superior y Linux de 64 bits (x86_64) con distribuciones "
        "Ubuntu 22.04 o superior y Fedora 39 o superior. No se admite el uso de clientes VPN "
        "de terceros.",
    ]),
    ("Instalación y conexión a CóndorVPN", [
        "4. Instalación del cliente",
        "Descargue el instalador desde el portal de autoservicio (autoservicio.itc.example), en la "
        "sección Software. En equipos administrados por el ITC el cliente ya viene instalado. En "
        "equipos personales, la instalación la hace el propio usuario y debe aceptar la política "
        "de uso aceptable antes de la primera conexión.",
        "5. Conexión",
        "Abra CóndorVPN, escriba la dirección del servidor vpn.itc.example y su usuario "
        "institucional (sin el dominio). Al ingresar la contraseña, el sistema enviará una "
        "notificación a CóndorAuth que debe aprobar en menos de 60 segundos. La conexión usa el "
        "protocolo IKEv2 por los puertos UDP 500 y UDP 4500; si la red desde la que se conecta "
        "bloquea esos puertos, el cliente cambia automáticamente a TLS por el puerto TCP 443.",
        "6. Límites de uso",
        "Cada usuario puede tener como máximo 3 dispositivos conectados a la VPN de forma "
        "simultánea. Al intentar conectar un cuarto dispositivo, la sesión más antigua se cierra "
        "automáticamente. Las sesiones inactivas se desconectan después de 2 horas sin tráfico, y "
        "toda sesión se cierra obligatoriamente a las 12 horas de iniciada, aunque esté en uso.",
        "La VPN usa túnel dividido: solo el tráfico hacia los servicios internos del ITC pasa por "
        "la VPN; la navegación general en internet sale por la conexión del usuario.",
    ]),
    ("Códigos de error de CóndorVPN", [
        "7. Errores frecuentes y cómo resolverlos",
        "E-401 - Credenciales inválidas. El usuario o la contraseña son incorrectos. Verifique "
        "que no esté escribiendo el dominio en el campo de usuario. Tenga en cuenta que los "
        "intentos fallidos en la VPN cuentan para el bloqueo de la cuenta institucional.",
        "E-403 - Acceso no autorizado. La cuenta no tiene permiso de VPN; es el caso de los "
        "estudiantes y de los contratistas cuya solicitud de acceso remoto no fue aprobada por su "
        "supervisor. Solicite el permiso por el catálogo de servicios.",
        "E-412 - MFA no aprobada. La notificación de CóndorAuth no fue aprobada a tiempo o fue "
        "rechazada. Reintente la conexión y apruebe la notificación en menos de 60 segundos.",
        "E-509 - Certificado de dispositivo vencido. Los certificados de dispositivo tienen una "
        "vigencia de 365 días. Para renovarlo, ingrese al portal de autoservicio "
        "(autoservicio.itc.example), opción Dispositivos, y pulse Renovar certificado; luego "
        "reinicie el cliente CóndorVPN.",
        "E-610 - Límite de sesiones alcanzado. Ya tiene 3 dispositivos conectados y la política "
        "de su grupo impide cerrar la sesión más antigua. Desconecte otro dispositivo.",
        "Si el error persiste después de seguir estas indicaciones, abra un caso en la mesa de "
        "ayuda indicando el código de error, el sistema operativo y la hora del intento.",
    ]),
    ("Redes inalámbricas del campus", [
        "8. Redes disponibles",
        "ITC-Seguro: red cifrada con WPA2-Enterprise para funcionarios, docentes, contratistas y "
        "estudiantes. Se ingresa con el usuario y la contraseña institucionales. Permite hasta 5 "
        "dispositivos por usuario.",
        "ITC-Invitados: red para visitantes. El acceso se obtiene con un código que genera la "
        "recepción de cada edificio; el código vence a las 8 horas y la velocidad está limitada "
        "a 10 Mbps por dispositivo. Desde ITC-Invitados no se puede acceder a servicios internos "
        "ni conectarse a la VPN.",
        "ITC-IoT: red reservada para impresoras, pantallas y sensores. Los usuarios no pueden "
        "conectarse a ella; los dispositivos se registran por solicitud a la mesa de ayuda.",
        "9. Problemas frecuentes con Wi-Fi",
        "Si su equipo no se conecta a ITC-Seguro después de un cambio de contraseña, olvide la red "
        "en el dispositivo y vuelva a conectarse con la contraseña nueva. Si la contraseña "
        "institucional caducó, el acceso a ITC-Seguro también queda bloqueado hasta que la cambie "
        "en el portal de autoservicio.",
    ]),
]

# ---------------------------------------------------------------------------
# 2. DOCX: Política de cuentas y contraseñas.
# ---------------------------------------------------------------------------
POLITICA = [
    ("Objeto y alcance", [
        "Esta política define las reglas para crear, proteger, bloquear y desactivar las cuentas "
        "institucionales del Instituto Tecnológico Cóndor (ITC). Aplica a funcionarios, docentes, "
        "estudiantes y contratistas, y a todos los servicios que usan la cuenta institucional: "
        "correo, CóndorDrive, VPN, Wi-Fi ITC-Seguro y sistemas administrativos.",
        "La Oficina de Seguridad de la Información es responsable de esta política. La mesa de "
        "ayuda de TI es responsable de aplicarla en la atención a los usuarios.",
    ]),
    ("Requisitos de las contraseñas", [
        "Las contraseñas deben tener una longitud mínima de 14 caracteres. Se recomienda usar "
        "frases de contraseña de varias palabras. No es obligatorio combinar mayúsculas, números "
        "y símbolos, pero la contraseña no puede contener el nombre de usuario ni el nombre o "
        "apellido del titular.",
        "Las contraseñas caducan cada 180 días. El sistema avisa por correo 14 días antes del "
        "vencimiento. No se puede reutilizar ninguna de las últimas 10 contraseñas.",
        "Las cuentas de servicio y las cuentas administrativas tienen requisitos más estrictos "
        "definidos en el estándar técnico de cuentas privilegiadas, que no hace parte de este "
        "documento.",
    ]),
    ("Autenticación de dos factores (MFA)", [
        "La autenticación de dos factores es obligatoria para todas las cuentas desde el primer "
        "inicio de sesión. El único método admitido es la aplicación CóndorAuth en un teléfono "
        "móvil; no se admiten mensajes de texto (SMS) ni llamadas.",
        "El portal de autoservicio (autoservicio.itc.example) exige una aprobación en CóndorAuth "
        "para cualquier operación sobre la cuenta o sus dispositivos, incluida la renovación de "
        "certificados de dispositivo y el cambio de contraseña.",
        "Si el usuario cambió de teléfono o perdió el dispositivo con CóndorAuth, no podrá usar el "
        "portal de autoservicio. En ese caso debe presentarse en la mesa de ayuda con su documento "
        "de identidad para que un técnico reinicie el enrolamiento de MFA. Este trámite no se "
        "atiende por teléfono ni por correo.",
    ]),
    ("Bloqueo y desbloqueo de cuentas", [
        "Una cuenta se bloquea automáticamente después de 5 intentos de inicio de sesión fallidos "
        "en un período de 15 minutos. Cuentan los intentos fallidos en cualquier servicio que use "
        "la cuenta institucional, incluida la VPN.",
        "El bloqueo automático se levanta solo después de 30 minutos. Si el usuario necesita el "
        "desbloqueo antes, puede pedirlo a la mesa de ayuda, que verificará su identidad con el "
        "código de empleado o de estudiante y la fecha de nacimiento registrada.",
        "Si una cuenta se bloquea 3 veces en un mismo día, el desbloqueo deja de ser automático y "
        "solo puede hacerlo la mesa de ayuda, que además notifica a la Oficina de Seguridad de la "
        "Información para revisar un posible intento de acceso no autorizado.",
    ]),
    ("Cuentas de contratistas e invitados", [
        "Las cuentas de contratistas se crean por solicitud del supervisor del contrato y vencen "
        "en la fecha de terminación del contrato, con una vigencia máxima de 90 días. Para "
        "extenderla, el supervisor debe pedir la renovación antes del vencimiento.",
        "Los contratistas no tienen acceso a la VPN por defecto. El supervisor debe solicitar el "
        "permiso de acceso remoto en el catálogo de servicios, indicando la justificación.",
        "Los visitantes no reciben cuenta institucional; usan la red ITC-Invitados.",
    ]),
    ("Desactivación de cuentas", [
        "Cuando un funcionario se retira del ITC, su cuenta se desactiva el último día laboral. El "
        "contenido de su correo y de CóndorDrive se conserva durante 30 días, período en el que el "
        "jefe inmediato puede solicitar que se transfiera a otra cuenta. Después de 30 días el "
        "contenido se elimina de forma definitiva.",
        "Las cuentas de estudiantes se desactivan 6 meses después de la graduación o del retiro.",
    ]),
]

# ---------------------------------------------------------------------------
# 3. DOCX: Catálogo de servicios y acuerdos de nivel de servicio (SLA).
# ---------------------------------------------------------------------------
CATALOGO = [
    ("Introducción", [
        "Este catálogo describe los servicios que presta la mesa de ayuda de TI del Instituto "
        "Tecnológico Cóndor (ITC), los canales de atención y los acuerdos de nivel de servicio "
        "(SLA) que la mesa se compromete a cumplir. Los tiempos se cuentan desde el registro del "
        "caso en el sistema de casos.",
    ]),
    ("Canales y horario de atención", [
        "La mesa de ayuda atiende de lunes a viernes de 7:00 a 19:00 y los sábados de 8:00 a "
        "12:00, excepto festivos. Los canales son: el portal de soporte (soporte.itc.example), "
        "el correo mesadeayuda@itc.example, la extensión telefónica 4000 y la atención presencial "
        "en el edificio B, oficina 104.",
        "Fuera de ese horario solo se atienden casos de prioridad P1, a través de la línea de "
        "guardia en la extensión 5000 (o el número externo 601-555-5000). Los casos de otras "
        "prioridades registrados fuera de horario se atienden al inicio de la siguiente jornada.",
    ]),
    ("Niveles de prioridad", [
        "P1 - Crítica: el incidente detiene un servicio para toda una dependencia o compromete la "
        "seguridad de la información, por ejemplo la caída del sistema financiero.",
        "P2 - Alta: el incidente impide trabajar a un usuario y no existe una alternativa, por "
        "ejemplo un equipo que no enciende.",
        "P3 - Media: el incidente afecta el trabajo de un usuario pero existe una alternativa "
        "temporal, por ejemplo una impresora que no funciona cuando hay otra disponible.",
        "P4 - Baja: solicitudes de servicio y consultas, como instalar software, crear una carpeta "
        "compartida o pedir información.",
    ]),
    ("Tiempos de respuesta y de resolución", [
        "P1: primera respuesta en 15 minutos y resolución objetivo en 4 horas, en cualquier día y "
        "hora (24x7).",
        "P2: primera respuesta en 1 hora hábil y resolución objetivo en 8 horas hábiles.",
        "P3: primera respuesta en 4 horas hábiles y resolución objetivo en 3 días hábiles.",
        "P4: primera respuesta en 1 día hábil y resolución objetivo en 10 días hábiles.",
        "Las horas hábiles son las del horario de atención de la mesa. La meta de cumplimiento del "
        "SLA es del 95 % de los casos de cada prioridad en cada mes.",
    ]),
    ("Escalamiento", [
        "Los casos los recibe el nivel 1. Si el nivel 1 no resuelve un caso P1 en 30 minutos, o "
        "un caso P2 en 2 horas hábiles, lo escala al nivel 2 (especialistas de infraestructura, "
        "redes o aplicaciones). Si el nivel 2 no resuelve un caso P1 en 2 horas, se notifica al "
        "coordinador de la mesa y se activa el comité de crisis.",
        "El usuario puede pedir el escalamiento de un caso respondiendo al correo de seguimiento "
        "con la palabra ESCALAR en el asunto.",
    ]),
    ("Servicios del catálogo", [
        "Instalación de software: se atiende como P4 y requiere la aprobación del jefe inmediato. "
        "Solo se instala software licenciado por el ITC o de licencia libre aprobado por la "
        "Oficina de Seguridad de la Información.",
        "Préstamo de equipos portátiles: hasta 5 días hábiles, con solicitud de al menos 2 días "
        "hábiles de anticipación.",
        "Creación de carpetas compartidas departamentales: P4, con aprobación del jefe de la "
        "dependencia propietaria.",
        "Acceso remoto (VPN) para contratistas: P4, con aprobación del supervisor del contrato.",
    ]),
    ("Encuestas de satisfacción", [
        "Al cerrar un caso, el usuario recibe una encuesta de satisfacción de 3 preguntas. Si "
        "califica la atención con 2 o menos sobre 5, el coordinador de la mesa revisa el caso y "
        "contacta al usuario en un plazo de 2 días hábiles.",
    ]),
]

# ---------------------------------------------------------------------------
# 4. Markdown: Preguntas frecuentes.
# ---------------------------------------------------------------------------
FAQ = f"""# Preguntas frecuentes - Mesa de Ayuda de TI

> {AVISO}

## Cómo pedir ayuda

**¿Cómo abro un caso?**
Por el portal de soporte (soporte.itc.example), por correo a mesadeayuda@itc.example, por la
extensión 4000 o en persona en el edificio B, oficina 104. El portal es el canal recomendado
porque permite adjuntar capturas de pantalla y seguir el estado del caso.

**¿Qué datos debo incluir en el caso?**
Su usuario institucional, una descripción del problema, desde cuándo ocurre, el código de error
si aparece y el nombre del equipo (está en una etiqueta en la parte inferior).

**¿Quién decide la prioridad de mi caso?**
El técnico de nivel 1 asigna la prioridad al registrar el caso, según la tabla de clasificación
de esta guía. El usuario puede pedir una revisión si no está de acuerdo.

## Clasificación de incidentes comunes

| Incidente | Prioridad |
|---|---|
| Pérdida o robo de un equipo portátil o teléfono con información institucional | P1 |
| Caída del correo o de CóndorDrive para toda una dependencia | P1 |
| Cuenta bloqueada | P2 |
| No puedo conectarme a la VPN y necesito un sistema interno para trabajar | P2 |
| Impresora averiada con otra impresora disponible | P3 |
| Lentitud del equipo | P3 |
| Instalación de software | P4 |
| Solicitud de carpeta compartida | P4 |

## Cuentas y contraseñas

**Olvidé mi contraseña, ¿qué hago?**
Cámbiela en el portal de autoservicio (autoservicio.itc.example) con la opción "Olvidé mi
contraseña". Necesitará aprobar la operación en CóndorAuth.

**Me cambié de teléfono y ya no tengo CóndorAuth.**
Acérquese a la mesa de ayuda con su documento de identidad para reiniciar el enrolamiento de MFA.

## Correo y almacenamiento

**¿Cuánto espacio tengo en el correo?**
Cada buzón tiene 50 GB. Al llegar al 90 % recibirá un aviso; al llenarse, no podrá enviar
mensajes hasta liberar espacio.

**¿Cuál es el tamaño máximo de los adjuntos?**
Los mensajes pueden tener como máximo 25 MB en adjuntos, tanto al enviar como al recibir. Para
archivos más grandes, comparta un enlace de CóndorDrive.

**¿Cuánto espacio tengo en CóndorDrive?**
Cada usuario tiene 100 GB. Los archivos en la papelera se eliminan de forma definitiva a los 30
días.

## Equipos y software

**Perdí mi portátil o me lo robaron, ¿qué hago?**
Repórtelo de inmediato a la mesa de ayuda: se registra como P1 y el equipo se bloquea de forma
remota. Además, debe informar a la Oficina de Seguridad de la Información dentro de las 2 horas
siguientes a que note la pérdida, y presentar la denuncia ante las autoridades si fue un robo.

**¿Puedo instalar programas en mi equipo?**
No. Los equipos institucionales no permiten instalar software sin permisos de administrador.
Pida la instalación por el catálogo de servicios; requiere la aprobación de su jefe inmediato.

**¿Cómo imprimo desde mi portátil personal?**
No es posible: la impresión solo está habilitada para equipos institucionales conectados a
ITC-Seguro o a la red cableada.

## Seguridad

**Recibí un correo sospechoso, ¿qué hago?**
No haga clic en los enlaces ni abra los adjuntos. Reenvíelo como adjunto a
seguridad@itc.example y luego elimínelo.
"""


# ---------------------------------------------------------------------------
# 5. DOCX: Procedimiento de incidentes de seguridad (documento "distractor":
#    comparte vocabulario con los demás, pero no responde las preguntas de prueba).
# ---------------------------------------------------------------------------
SEGURIDAD = [
    ("Objetivo", [
        "Este procedimiento describe cómo la Oficina de Seguridad de la Información del Instituto "
        "Tecnológico Cóndor (ITC) identifica, contiene y cierra los incidentes de seguridad. "
        "Complementa la política de cuentas y contraseñas y el catálogo de servicios de la mesa de "
        "ayuda, pero tiene su propio flujo de trabajo y su propio equipo de respuesta.",
        "Un incidente de seguridad es cualquier evento que comprometa o pueda comprometer la "
        "confidencialidad, la integridad o la disponibilidad de la información institucional.",
    ]),
    ("Tipos de incidentes", [
        "Suplantación (phishing): correos, mensajes o llamadas que intentan obtener credenciales o "
        "convencer al usuario de ejecutar un archivo. Es el tipo de incidente más reportado en el ITC.",
        "Código malicioso: virus, ransomware o programas no autorizados detectados por el antivirus "
        "institucional CóndorShield o reportados por el usuario.",
        "Acceso no autorizado: uso de una cuenta por alguien distinto a su titular, o acceso a "
        "carpetas o sistemas sin la autorización correspondiente.",
        "Fuga de información: envío, publicación o copia de información clasificada como "
        "confidencial o restringida fuera de los canales autorizados.",
        "Pérdida de activos: extravío o robo de equipos, memorias o documentos que contengan "
        "información institucional.",
    ]),
    ("Clasificación de la información", [
        "Pública: información que puede divulgarse sin restricción, como los programas académicos "
        "publicados en el sitio web.",
        "Interna: información de uso general dentro del ITC, como los manuales y procedimientos de "
        "la mesa de ayuda.",
        "Confidencial: información cuyo acceso está limitado a una dependencia, como las nóminas, "
        "las calificaciones y los contratos.",
        "Restringida: información cuyo acceso está limitado a personas nombradas individualmente, "
        "como las credenciales de cuentas privilegiadas y los informes de auditoría.",
        "La información confidencial y restringida solo puede almacenarse en CóndorDrive o en las "
        "carpetas compartidas departamentales; no puede guardarse en memorias USB sin cifrar ni en "
        "servicios de almacenamiento personales.",
    ]),
    ("Controles en los equipos", [
        "Todos los portátiles institucionales tienen el disco cifrado: BitLocker en Windows y "
        "FileVault en macOS. El cifrado se activa en la entrega del equipo y el usuario no puede "
        "desactivarlo.",
        "Los puertos USB de los equipos institucionales solo aceptan memorias cifradas entregadas "
        "por el ITC. Las memorias personales se bloquean automáticamente.",
        "Los equipos institucionales pueden bloquearse y borrarse de forma remota. La Oficina de "
        "Seguridad ordena el borrado remoto de un equipo perdido si no se recupera en 72 horas.",
        "El antivirus CóndorShield se actualiza cada 4 horas. Si un equipo pasa más de 7 días sin "
        "actualizarse, pierde el acceso a la red ITC-Seguro hasta que se conecte por cable y se "
        "actualice.",
    ]),
    ("Fases de la respuesta", [
        "Detección y registro: el incidente se registra en el sistema de la Oficina de Seguridad "
        "con el formulario de incidentes (seguridad.itc.example/reportar) o por el correo "
        "seguridad@itc.example. Cada incidente recibe un código con el formato SEG-año-número.",
        "Contención: el equipo de respuesta aísla los equipos afectados, revoca las sesiones "
        "abiertas de las cuentas comprometidas y fuerza el cambio de contraseña cuando corresponde.",
        "Erradicación y recuperación: se elimina la causa del incidente y se restauran los "
        "servicios desde las copias de seguridad, que se hacen cada noche y se conservan 35 días.",
        "Cierre y lecciones aprendidas: los incidentes de severidad alta se revisan en una reunión "
        "de lecciones aprendidas dentro de los 10 días hábiles siguientes al cierre.",
    ]),
    ("Severidad", [
        "La Oficina de Seguridad usa una escala propia de severidad (baja, media, alta y crítica), "
        "distinta de las prioridades P1 a P4 de la mesa de ayuda. La severidad depende de la "
        "clasificación de la información afectada y del número de usuarios comprometidos.",
        "Un incidente que afecte información restringida es siempre de severidad crítica. Los "
        "incidentes críticos se informan a la rectoría el mismo día.",
    ]),
    ("Responsabilidades de los usuarios", [
        "Reportar de inmediato cualquier sospecha de incidente, aunque no esté seguro de que lo sea.",
        "No intentar investigar ni corregir por su cuenta un incidente, por ejemplo borrando "
        "correos sospechosos de otros buzones o desconectando servidores.",
        "Conservar la evidencia: no apagar un equipo infectado, desconectarlo de la red y esperar "
        "las indicaciones del equipo de respuesta.",
        "Completar cada año el curso virtual de seguridad de la información, que tiene una "
        "duración de 2 horas y se aprueba con 80 % de respuestas correctas.",
    ]),
]

# ---------------------------------------------------------------------------
# 6. Markdown: Guía de equipos, impresión y software (documento "distractor").
# ---------------------------------------------------------------------------
GUIA_EQUIPOS = f"""# Guía de equipos, impresión y software

> {AVISO}

## Equipos institucionales

Cada funcionario y docente de planta recibe un portátil institucional. Los equipos se renuevan
cada 4 años; la mesa de ayuda avisa con un mes de anticipación para programar la entrega del
equipo nuevo y la copia de los archivos.

Los equipos tienen garantía del fabricante durante 3 años. Si el equipo falla dentro de la
garantía, la mesa de ayuda gestiona la reparación y entrega un equipo de reemplazo mientras tanto.

No está permitido cambiar piezas, abrir el equipo ni instalar otro sistema operativo. Los daños
por golpes o líquidos los evalúa la mesa de ayuda antes de enviar el equipo a reparación.

## Préstamo de equipos

La mesa de ayuda presta portátiles, proyectores y cámaras para eventos y trabajo temporal. Los
portátiles se prestan hasta por 5 días hábiles. Los proyectores y las cámaras se prestan por
jornada y se devuelven el mismo día antes de las 18:00.

Al recibir un equipo prestado, el usuario firma un acta de entrega. Si el equipo se devuelve con
daños, el caso se reporta al jefe de la dependencia.

## Impresión

Las impresoras multifuncionales están en todos los edificios. Para imprimir, envíe el documento a
la cola "ITC-Impresion" y retírelo en cualquier impresora acercando su carné; los trabajos que no
se retiran en 24 horas se eliminan de la cola.

Cada funcionario tiene una cuota de 300 páginas en blanco y negro al mes. La impresión a color
requiere la aprobación del jefe de la dependencia y se descuenta como 5 páginas por cada página
a color.

Los escáneres de las multifuncionales envían los documentos al correo del usuario en formato
PDF, con un máximo de 50 páginas por trabajo.

## Software disponible

Todos los equipos institucionales incluyen la suite de ofimática, el navegador, el cliente de
correo, CóndorDrive, CóndorAuth para escritorio, el cliente CóndorVPN y el antivirus CóndorShield.

El software especializado (estadística, diseño, desarrollo) se instala por solicitud en el
catálogo de servicios. Las licencias son institucionales y no pueden instalarse en equipos
personales, salvo la suite de ofimática, que cada usuario puede instalar en hasta 5 equipos
personales mientras tenga cuenta activa.

## Actualizaciones

Las actualizaciones de seguridad se publican el segundo martes de cada mes. Los equipos las
descargan automáticamente y el usuario tiene 7 días para reiniciar; después de ese plazo el
equipo se reinicia solo a las 20:00.

Antes de una actualización mayor del sistema operativo, la mesa de ayuda envía un correo con la
fecha programada y las instrucciones para guardar el trabajo.

## Salas de cómputo

Las salas de cómputo de los edificios A y C abren de lunes a viernes de 7:00 a 21:00. Los
estudiantes ingresan con su cuenta institucional y sus archivos se borran al cerrar la sesión;
para conservarlos deben guardarlos en CóndorDrive.
"""


def generar_pdf(ruta: Path) -> None:
    pdf = FPDF(format="A4")
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=False)
    for titulo, parrafos in MANUAL_VPN:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 15)
        pdf.multi_cell(0, 8, titulo)
        pdf.ln(3)
        for p in parrafos:
            es_subtitulo = p[:2].strip().rstrip(".").isdigit() and len(p) < 60
            pdf.set_font("Helvetica", "B" if es_subtitulo else "", 12 if es_subtitulo else 10.5)
            pdf.multi_cell(0, 5.5, p)
            pdf.ln(2.5)
        pdf.set_y(-15)
        pdf.set_font("Helvetica", "I", 8)
        pdf.cell(0, 5, f"ITC - Manual de conectividad - página {pdf.page_no()}", align="C")
    pdf.output(str(ruta))


def generar_docx(ruta: Path, titulo: str, secciones) -> None:
    doc = Document()
    doc.add_heading(titulo, level=0)
    doc.add_paragraph().add_run(AVISO).italic = True
    for i, (nombre, parrafos) in enumerate(secciones, start=1):
        doc.add_heading(f"{i}. {nombre}", level=1)
        for p in parrafos:
            doc.add_paragraph(p)
    doc.save(str(ruta))


def main() -> None:
    CORPUS.mkdir(exist_ok=True)
    generar_pdf(CORPUS / "manual_conectividad_vpn.pdf")
    generar_docx(CORPUS / "politica_cuentas_contrasenas.docx",
                 "Política de cuentas institucionales y contraseñas", POLITICA)
    generar_docx(CORPUS / "catalogo_servicios_sla.docx",
                 "Catálogo de servicios y acuerdos de nivel de servicio", CATALOGO)
    (CORPUS / "faq_mesa_ayuda.md").write_text(FAQ, encoding="utf-8")
    generar_docx(CORPUS / "procedimiento_incidentes_seguridad.docx",
                 "Procedimiento de gestión de incidentes de seguridad de la información", SEGURIDAD)
    (CORPUS / "guia_equipos_impresion_software.md").write_text(GUIA_EQUIPOS, encoding="utf-8")
    print("Corpus generado en", CORPUS)
    for f in sorted(CORPUS.iterdir()):
        print(" -", f.name, f.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
