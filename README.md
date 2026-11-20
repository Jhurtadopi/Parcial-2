# Proyecto RAG — Asistente de Mesa de Ayuda de TI

Parcial práctico de Sistemas Inteligentes Computacionales (Corte 2). Es un asistente RAG que responde preguntas sobre los documentos de una mesa de ayuda de TI, cita la evidencia (archivo y localizador) y se abstiene cuando la evidencia no alcanza.

> **Corpus sintético.** El "Instituto Tecnológico Cóndor" es ficticio. Todos los documentos de `corpus/` los generó `herramientas/generar_corpus.py` y están marcados como sintéticos. No contienen datos reales ni personales, así que se pueden enviar a OpenRouter sin problema.

## Estructura

| Ruta | Contenido |
|---|---|
| `proyecto_rag.ipynb` | Cuaderno ejecutable: ingesta, fragmentación, índice, recuperación, LLM, corridas y métricas |
| `corpus/` | 6 documentos: 1 PDF, 3 DOCX y 2 MD |
| `herramientas/generar_corpus.py` | Regenera el corpus sintético (es determinista) |
| `evaluacion/preguntas.json` | Las 9 preguntas de referencia, con su respuesta esperada y la evidencia literal |
| `evaluacion/valoracion_*.csv` | Valoraciones de los evaluadores (se crean después de las corridas) |
| `resultados/` | `corridas.jsonl`, `fallos.jsonl`, `registro_corridas.csv`, `tabla_resultados.csv`, `prompts.json`, `entorno.json` |
| `plantillas/` | Plantillas del equipo: caso de uso, hipótesis, rúbrica, estructura del informe, etc. |
| `PLAN_TRABAJO.md` | Reparto del trabajo y cronograma |

## Ejecutar en Google Colab

1. Sube el proyecto a Colab de una de estas dos formas:
   - Pon la URL del repositorio en `REPO_URL` (celda 1).
   - Comprime la carpeta como `proyecto_rag.zip` y súbela cuando la celda 1 lo pida.
2. En el panel 🔑 **Secretos** de Colab, crea `OPENROUTER_API_KEY` con tu clave y dale acceso al cuaderno. **No escribas la clave en ninguna celda.**
3. Ejecuta **Entorno de ejecución → Ejecutar todas**. Las dependencias se instalan solas.
4. Las corridas finales están apagadas por defecto. Para lanzarlas, pon `EJECUTAR_CORRIDAS = True` en la sección 9. Si se interrumpen, por ejemplo por el límite de solicitudes de los modelos gratuitos, vuelve a ejecutar la celda y continúa donde quedó.

## Ejecutar en local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # y pon tu clave en .env (está en .gitignore)
jupyter notebook proyecto_rag.ipynb
```

## Configuraciones

| Config | Cambio respecto a R0 |
|---|---|
| R0 | Fragmentos fijos de 400 tokens con 60 de solapamiento, `multilingual-e5-small`, coseno, k = 4 |
| R1 | Fragmentos fijos de 200 tokens con 30 de solapamiento (misma proporción, 15 %) |
| R2 | k = 8 |
| C0 | Sin recuperación: mismo LLM, sin documentos |
| B_EMB | Embeddings `BAAI/bge-m3` (se reconstruye el índice) |
| B_LLM | LLM `nvidia/nemotron-3-ultra-550b-a55b:free` |

Parámetros que no cambian entre configuraciones: temperatura 0, 512 tokens de salida, 2400 tokens de contexto, semilla 42 y razonamiento desactivado.

- **LLM principal:** `google/gemma-4-31b-it:free` (OpenRouter).
- **Modelos gratuitos:** los IDs de OpenRouter cambian con el tiempo. La sección 6 del cuaderno comprueba que los modelos configurados existan y, si no, lista las alternativas.

## Pendiente del equipo antes de las corridas finales

- [ ] Revisar y **congelar** `evaluacion/preguntas.json` con un commit fechado.
- [ ] Escribir y fechar las hipótesis en `plantillas/hipotesis.md`.
- [ ] Después de las corridas: dos evaluadores llenan `valoracion_e1.csv` y `valoracion_e2.csv`, resuelven los desacuerdos y guardan el consenso en `valoracion_final.csv`.
