# Reglas del Asistente - Proyecto RAG (Mesa de Ayuda de TI)

Contexto: proyecto académico RAG (Mesa de Ayuda de TI). Lee README.md, PLAN_TRABAJO.md y Enunciado_Proyecto_RAG.md.

## Reglas permanentes:
1. Nunca leas, imprimas ni agregues a git el archivo .env ni ninguna clave.
2. No cambies los parámetros fijos (temperatura 0, 512 tokens de salida, 2400 de contexto, semilla 42, prompts, modelos) salvo que yo lo pida.
3. Después del tag "congelado" no modifiques evaluacion/preguntas.json ni plantillas/hipotesis.md.
4. Antes de ejecutar algo que llame al LLM, dime cuántas llamadas serán y espera mi OK.
5. No hagas git commit ni git push. Yo hago los commits.
6. Trabaja los experimentos sobre copias en scratch/ y no modifiques el cuaderno original salvo que te lo pida.
7. Explícame en español simple qué hiciste y por qué: tengo que sustentarlo sin IA.
8. Al terminar cada tarea, agrega una entrada a informe/bitacora_ia.md con fecha, herramienta, tarea solicitada, qué generó/modificó y validación realizada.
