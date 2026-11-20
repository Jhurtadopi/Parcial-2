**SISTEMAS INTELIGENTES COMPUTACIONALES** 

**Parcial Practico Sustentable sobre sistemas RAG (Corte 2\)** 

En equipos de tres personas construyan un asistente que responda preguntas sobre una  colección de documentos, cite la evidencia y se abstenga cuando esta sea insuficiente. RAG  significa generación aumentada por recuperación. Antes de llamar al modelo de lenguaje  (LLM), el sistema busca fragmentos relevantes y los incorpora como contexto. 

Es necesario elegir un caso de aplicación, podría ser una Mesa de Ayuda que necesita  consultar manuales, guías y preguntas frecuentes para resolver incidencias, un Asistente  para consultar documentación de un proyecto de software, u otro caso de aplicación en el  área de informática que se les ocurra. Definan quién usará el sistema, qué preguntas debe  resolver y qué asuntos quedan fuera del alcance. Reúnan documentos públicos, autorizados  para el uso previsto o sintéticos identificados como tales. 

**1\. Requisitos mínimos del prototipo** 

• **Ingesta.** Procesen en una misma colección al menos tres archivos con contenido distinto  y en dos formatos diferentes, por ejemplo: PDF con texto seleccionable, DOCX, MD.  Pueden seleccionar y cargar varios archivos juntos o configurar una carpeta para que el  sistema los lea automáticamente al iniciar. 

• **Indexación y búsqueda.** Extraigan el texto y divídanlo en fragmentos. Conserven el  archivo de origen y un localizador verificable, como página, sección, párrafo o líneas.  Construyan un índice de embeddings y usen el mismo modelo de embeddings para  documentos y consultas dentro de cada configuración. 

• **Consulta y trazabilidad.** Reciban preguntas en lenguaje natural. Muestren la respuesta,  los fragmentos recuperados en orden y las citas que vinculan las afirmaciones con  archivo y localizador. El sistema debe indicar cuándo la evidencia es insuficiente.  

• **Modelos y ejecución.** Usen al menos un LLM de Hugging Face, OpenRouter o un  proveedor con clave API propia. Pueden ejecutar un modelo de Hugging Face  localmente y usar embeddings locales o de otro proveedor. Registren los identificadores  de los modelos. Guarden las claves en variables de entorno o secretos del entorno de  ejecución. Usen solo datos aptos para el procesamiento por servicios externos. 

**2\. Ruta de trabajo**   
Primero, definan el caso y construyan la configuración base. Luego, implementen las  variantes y prueben con preguntas de desarrollo. Por último, ejecuten la evaluación final y  preparen la sustentación. 

**3\. Configuraciones y experimentos**   
**A.** Implementen una configuración base, dos variantes y un control, teniendo en cuenta la  siguiente tabla. Antes de ejecutar las pruebas finales, documenten qué esperan que  cambie en cada comparación y por qué.

Proyecto RAG / 1 

| Configuración Qué debe cambiar Qué permite observar |  |  |
| ----- | :---- | :---- |
| **R0 · Base** | Fragmentos de tamaño fijo con solapamiento,  embeddings, similitud coseno y los k primeros  resultados. Como punto de partida, usen, por  ejemplo, 400 tokens, 60 de solapamiento y k \= 4\. | Establece una referencia para  medir la recuperación y las  respuestas. |
| **R1 · Fragmentación** | Cambien solo el tamaño de fragmento con la  misma proporción de solapamiento, o cambien a  cortes por párrafo o sección con un límite similar.  Declaren la regla y vuelvan a indexar. | Permite observar si la evidencia  queda cortada, se conserva  unida o llega acompañada de  texto irrelevante. |
| **R2 · Recuperación** | Sobre R0, cambien solo k (por ejemplo, de 4 a 8\)  o comparen la búsqueda densa con una  búsqueda híbrida que combine la densa con otro  mecanismo. Si eligen la búsqueda híbrida,  conserven k. | Permite medir el efecto de  ampliar la selección o de   combinar similitud semántica  con coincidencias de términos. |
| **C0 · Control sin   recuperación** | Consulten el mismo LLM con las mismas  preguntas, sin documentos ni fragmentos (Sin  RAG). Pídanle responder con su conocimiento y  señalar si carece de información. No le pidan  citas documentales. | Permite comparar la corrección  de las respuestas y el   comportamiento cuando el LLM  carece de evidencia   documental. |

• Mantengan fijo el corpus, las preguntas, los modelos, la temperatura cuando sea  configurable y el límite de salida. Para R0, R1 y R2 usen además la misma plantilla de  instrucciones y el mismo límite máximo de contexto. Registren si el límite obliga a  recortar fragmentos. 

• Comparen R1 con R0 y R2 con R0 por separado. Comparen C0 con R0 en corrección de  las preguntas respondibles y en abstención ante preguntas sin respuesta en el corpus.  Indiquen que C0 tiene instrucciones de respuesta adaptadas a la ausencia de  documentos y que las citas solo se evalúan en las configuraciones RAG. 

• Documenten los parámetros efectivos, las unidades y el entorno de ejecución. Si el  proveedor no permite fijar la semilla o un parámetro, regístrenlo como límite de la  comparación. 

**B.** Probar otro modelo de embeddings y un LLM distinto como otro experimento, basándose  en R0. Como se cambian los embeddings, debe reconstruir el índice y codifiquen las  consultas con el nuevo modelo. Documente los resultados y su respectivo análisis. 

**4\. Protocolo de evaluación** 

• ***Preparación de las preguntas:*** antes de las corridas finales, fijen 9 preguntas con su  referencia. Incluyan 3 sobre un único documento (directas), 3 que exijan combinar  información de al menos dos documentos y 3 cuya respuesta no figure en la colección.  Para las 6 respondibles, registren la respuesta esperada y los textos necesarios con el  archivo y la ubicación de la respuesta, registren por escrito la evidencia. Para las otras 3,  justifiquen por qué el corpus no permite responder. 

• ***Ejecución y métricas:*** ejecuten las 9 preguntas en las cuatro configuraciones (parte A de Configuraciones y experimentos), para un mínimo de 36 corridas. Guarden pregunta,  configuración, fragmentos recuperados y contexto enviado cuando apliquen, respuesta,  citas, tiempo por consulta y valoración. Si una llamada falla, regístrenla y repítanla bajo  la misma configuración.

Proyecto RAG / 2 

| Indicador Cómo se calcula |  |
| ----- | :---- |
| **Cobertura  de   evidencia** | En las 6 preguntas respondibles, cuenten cuántas tienen todos los  pasajes necesarios entre los fragmentos recuperados y cuántas los  conservan en el contexto enviado al LLM. Reporten ambos conteos  sobre 6 para cada variante RAG. |
| **Corrección**  | En las 6 preguntas respondibles, cuenten cuántas respuestas son  correctas y completas frente a la referencia. Una respuesta parcial  o una abstención cuenta como incorrecta. Reporten el conteo sobre  6 en cada configuración. |
| **Respaldo   de las citas** | Entre las respuestas sustantivas de cada variante RAG, calculen la  proporción cuyas afirmaciones centrales están respaldadas por los  pasajes efectivamente citados. Una respuesta sustantiva aporta al   menos una afirmación que intenta contestar la pregunta. Si el  denominador es cero, reporten «no aplica». |
| **Abstención  apropiada** | En las 3 preguntas sin respuesta documental, cuenten cuántas  veces el sistema reconoce que no puede responder y evita añadir  una respuesta sin respaldo. Reporten el conteo sobre 3 por  configuración. |

• ***Análisis:*** presenten una tabla de resultados y el análisis de los efectos de las  modificaciones. 

**5\. Entrega y sustentación** 

**Productos del equipo (60% \- Grupal)**   
A más tardar el día 23 de noviembre a las 11:59 p.m. deben subir al Classroom una carpeta  con lo siguiente: 

• **Cuaderno listo para ejecución:** incluyan dependencias, pasos de instalación y  ejecución, corpus o instrucciones para obtenerlo, y configuraciones identificadas para  repetir la prueba. Documenten cómo configurar las credenciales sin entregar claves. 

• **Paquete de evaluación:** entreguen las preguntas con referencias, los registros de las  corridas. 

• **Informe:** incluyan el caso de uso, un esquema del flujo, las hipótesis, la tabla de  resultados, el análisis de los experimentos y la configuración recomendada. Si usaron IA  para programar o redactar, declaren las herramientas utilizadas, el uso especifico y la  forma en que validaron los aportes de la IA. 

**Sustentación individual (40% \- Individual)**   
La sustentación se realizará el día 25 de noviembre en el horario de clase. Cada integrante  tendrá que responder a preguntas que plantee el docente. Podrán consultar el documento  del informe presentado, como único recurso de apoyo. En el momento de la sustentación no  pueden usar asistencia generativa externa. Se darán turnos a cada equipo para la  sustentación.

Proyecto RAG / 3   
Proyecto RAG / 4