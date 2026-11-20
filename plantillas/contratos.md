# Contratos entre componentes

## Fragmento (A → B)
```python
{
  "chunk_id": "manual.pdf::p3::c2",
  "archivo": "manual.pdf",
  "formato": "pdf",
  "localizador": "p. 3",          # página | sección | párrafo | líneas 10-24
  "texto": "...",
  "n_tokens": 398,
  "config_fragmentacion": "R0"     # R0 | R1
}
```

## Resultado de recuperación (B)
```python
[{"chunk_id": "...", "puntaje": 0.82, "rango": 1}, ...]   # orden descendente
```

## Configuración
```python
{
  "nombre": "R0",
  "chunk_size": 400, "overlap": 60, "unidad": "tokens (<tokenizador>)",
  "k": 4, "tipo_busqueda": "densa",          # densa | hibrida
  "modelo_embeddings": "<id>", "modelo_llm": "<id>",
  "temperatura": 0, "max_tokens_salida": 512, "max_tokens_contexto": 2000,
  "plantilla_prompt": "prompts/rag_v1.txt", "semilla": null
}
```

## Registro de corrida (B → C)
Ver `registro_corridas.csv`. Detalle completo (contexto enviado, respuesta) en `corridas.jsonl` con el mismo `run_id`.
