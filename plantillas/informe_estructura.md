# Informe — Proyecto RAG

1. **Caso de uso**: usuarios, preguntas en alcance y fuera de alcance, corpus (origen y licencia).
2. **Esquema del flujo**: diagrama ingesta → fragmentación → embeddings → índice → recuperación → prompt → LLM → respuesta con citas / abstención.
3. **Implementación y entorno**: librerías, IDs de los modelos, parámetros efectivos con unidades, hardware o entorno, límites (semilla, etc.).
4. **Configuraciones**: tabla de R0, R1, R2, C0 y B con solo lo que cambia en cada una.
5. **Hipótesis**: copia de `hipotesis.md` con su fecha.
6. **Protocolo de evaluación**: preguntas (tipos), rúbrica y doble calificación.
7. **Resultados**: tabla con cobertura (recuperado/contexto), corrección, respaldo de citas, abstención y tiempo promedio por configuración.
8. **Análisis**: R1 vs R0, R2 vs R0, C0 vs R0 y parte B; ¿se cumplieron las hipótesis?; ejemplos concretos de aciertos y fallos.
9. **Configuración recomendada** y por qué.
10. **Limitaciones** (9 preguntas, una sola corrida, variabilidad del proveedor, etc.).
11. **Declaración de uso de IA**: herramientas, para qué se usó cada una y cómo se validaron sus aportes.

Anexos: preguntas de referencia, registro de corridas, instrucciones de ejecución.
