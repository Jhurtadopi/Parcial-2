# Proyecto RAG — Asistente de Mesa de Ayuda de TI

**Sistemas Inteligentes Computacionales · Parcial Práctico RAG (Corte 2)**

Asistente que responde preguntas sobre la colección documental de la mesa de ayuda de TI del Instituto Tecnológico Cóndor, **cita la evidencia** (archivo + localizador verificable) y **se abstiene** con la frase contractual `EVIDENCIA INSUFICIENTE:` cuando los documentos no contienen información suficiente.

> **Corpus Sintético:** La institución "Instituto Tecnológico Cóndor" (ITC) es ficticia. Todos los documentos de `corpus/` fueron generados de forma determinista mediante `herramientas/generar_corpus.py` y están debidamente rotulados como contenido sintético. No contienen datos reales ni información confidencial o personal, siendo plenamente aptos para su procesamiento mediante servicios externos (OpenRouter).

---

## 1. Mapa de Carpetas y Archivos

```text
├── README.md                           # Guía general de instalación, uso y configuraciones
├── requirements.txt                    # Dependencias congeladas para entorno Python
├── .env.example                        # Plantilla para variables de entorno (sin claves)
├── .gitignore                          # Exclusiones de Git (.env, indices/, __pycache__/, etc.)
├── proyecto_rag.ipynb                  # Cuaderno principal ejecutable (salidas limpias)
├── proyecto_rag_ejecutado.ipynb        # Cuaderno con las salidas de ejecución reproducidas
├── PLAN_TRABAJO.md                     # Plan de trabajo, roles, contratos y checklist
├── Enunciado_Proyecto_RAG.md           # Especificación académica del proyecto
│
├── corpus/                             # Colección documental sintética (≥ 3 archivos, ≥ 2 formatos)
│   ├── manual_conectividad_vpn.pdf     # Manual VPN y Wi-Fi (p. 1–4, con texto seleccionable)
│   ├── politica_cuentas_contrasenas.docx # Política de contraseñas, MFA y bloqueos (§ 1–6)
│   ├── catalogo_servicios_sla.docx     # Catálogo de servicios, prioridades P1–P4 y SLAs (§ 1–7)
│   ├── guia_equipos_impresion_software.md # Equipos, cuotas de impresión y software (§ 1–6)
│   ├── faq_mesa_ayuda.md               # Preguntas frecuentes y clasificación de casos (§ 1–4)
│   ├── procedimiento_incidentes_seguridad.docx # Protocolo de respuesta a incidentes (§ 1–6)
│   └── README.md                       # Documentación del origen y licencias del corpus
│
├── evaluacion/                         # Paquete de evaluación y referencias
│   ├── preguntas.json                  # 9 preguntas (3 D, 3 M, 3 N) con evidencia literal congelada
│   ├── preguntas_desarrollo.json       # Preguntas preliminares de exploración
│   ├── valoracion_plantilla.csv        # Plantilla tabular para doble evaluación a ciegas
│   └── valoracion_final.csv            # Calificaciones consensuadas y justificaciones
│
├── resultados/                         # Evidencias experimentales y resultados consolidados
│   ├── corridas.jsonl                  # Registro detallado de inferencias, fragmentos y respuestas
│   ├── registro_corridas.csv           # Resumen tabular de corridas ejecutadas
│   ├── tabla_resultados.csv            # Métricas agregadas exportadas por calcular_metricas()
│   ├── tabla_resultados.md             # Informe de resultados y matriz pregunta × configuración
│   ├── fallos.jsonl                    # Bitácora de fallos y reintentos (códigos HTTP 429)
│   ├── entorno.json                    # Registro de hardware, versiones de paquetes y parámetros
│   └── prompts.json                    # Prompts del sistema utilizados
│
├── informe/                            # Documentación gráfica y bitácora de desarrollo
│   ├── flujo.mmd                       # Diagrama de arquitectura del pipeline en Mermaid
│   ├── flujo.png                       # Imagen de alta resolución del flujo y sus variantes
│   └── bitacora_ia.md                  # Registro cronológico del uso y validación de IA (Sec. 11)
│
├── plantillas/                         # Contratos y documentos de diseño metodológico
│   ├── caso_de_uso.md                  # Especificación del caso, usuarios y alcance
│   ├── hipotesis.md                    # Hipótesis previas basadas exclusivamente en diseño
│   ├── rubrica_evaluacion.md           # Rúbrica oficial y guía de casos dudosos resueltos
│   ├── informe_estructura.md           # Estructura del informe final
│   └── contratos.md                    # Esquemas de datos entre componentes
│
└── herramientas/
    └── generar_corpus.py               # Generador determinista del corpus sintético
```

---

## 2. Gestión Segura de Credenciales (Sin entregar claves)

El proyecto requiere acceso a la API de **OpenRouter** únicamente si se van a realizar nuevas llamadas a modelos LLM (`EJECUTAR_CORRIDAS = True`). Para reproducir la evaluación y recalcular métricas (`EJECUTAR_CORRIDAS = False`), **no se requiere ninguna clave**.

### Reglas de Seguridad:
1. **Nunca escribas la clave API dentro de ninguna celda del cuaderno ni en archivos subidos a Git.**
2. El archivo `.env` está expresamente excluido en el `.gitignore`.

### Configuración en Google Colab:
1. Abre el panel lateral izquierdo y pulsa en el ícono de **Llave (🔑 Secretos)**.
2. Agrega un nuevo secreto con nombre `OPENROUTER_API_KEY` y pega tu clave privada.
3. Activa el interruptor **Acceso a bloc de notas**.
4. El cuaderno lee la clave automáticamente mediante `google.colab.userdata` sin mostrarla en pantalla.

### Configuración en Entorno Local:
Copia la plantilla y define la variable sin comprometerla en el control de versiones:
```bash
cp .env.example .env
# Edita .env y asigna tu clave: OPENROUTER_API_KEY=sk-or-v1-...
```
Alternativamente, puedes exportarla en tu terminal:
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

---

## 3. Instrucciones de Instalación y Ejecución

### Opción A: Google Colab (Recomendada)
1. Abre `proyecto_rag.ipynb` en Google Colab.
2. Sube el proyecto de una de estas dos formas:
   - Clona tu repositorio público/privado asignando `REPO_URL` en la Celda 2.
   - O sube el archivo comprimido `proyecto_rag.zip` cuando el entorno lo solicite.
3. Ejecuta **Entorno de ejecución → Ejecutar todas**.
4. Las dependencias requeridas (`pypdf`, `python-docx`, `sentence-transformers`, `openai`, `rank_bm25`) se instalarán automáticamente en la sesión.
5. El cuaderno procesará el corpus, indexará los vectores, cargará las corridas existentes y generará la tabla de métricas sin costo.

### Opción B: Entorno Local (Linux / macOS / Windows)
1. **Crear y activar el entorno virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate       # En Windows: .venv\Scripts\activate
   ```
2. **Instalar dependencias:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Iniciar Jupyter Notebook:**
   ```bash
   jupyter notebook proyecto_rag.ipynb
   ```
4. **Ejecutar el cuaderno:**
   - Con `EJECUTAR_CORRIDAS = False` (valor predeterminado): Recalcula y verifica métricas reutilizando `resultados/corridas.jsonl` de manera determinista e instantánea.
   - Con `EJECUTAR_CORRIDAS = True`: Lanza llamadas a OpenRouter para las configuraciones pendientes.

---

## 4. Configuraciones y Variantes del Sistema

| Configuración | Descripción técnica | Parámetros distintivos | Experimento |
|---|---|---|:---:|
| **R0** | Base RAG estándar | Chunks de 400 tok, solape 60, embeddings `e5-small` (384d), $k=4$, LLM Gemma 4 31B | A |
| **R1** | Fragmentación reducida | Chunks pequeños de 200 tok, solape 30 (15 %), resto idéntico a R0 | A |
| **R2** | Recuperación ampliada | Amplitud $k=8$ fragmentos, resto idéntico a R0 | A |
| **C0** | Línea base sin RAG | Sin recuperación ($k=0$), prompt directo al LLM sin documentos ni citas | A |
| **B_EMB** | Embeddings alternativos | Índice y consultas con `BAAI/bge-m3` (1024d), resto idéntico a R0 | B |
| **B_LLM** | LLM alternativo | Inferencia con `nvidia/nemotron-3-ultra-550b-a55b:free`, resto idéntico a R0 | B |
| *R2_HIBRIDA* | Búsqueda híbrida (opcional) | Recuperación combinada densa + BM25 mediante Reciprocal Rank Fusion (RRF), $k=4$ | — |

### Parámetros Fijos y Controlados:
- **Temperatura:** `0.0` (determinismo).
- **Semilla:** `42` (declarada al proveedor).
- **Límite de salida:** `512 tokens`.
- **Límite estricto de contexto:** `2400 tokens` (con recorte automático de fragmentos excedentes).
- **Razonamiento:** Desactivado (`{"enabled": False}`).

