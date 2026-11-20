# Bitácora de Uso de Inteligencia Artificial

Registro de interacciones con asistentes de IA para el proyecto RAG (Mesa de Ayuda de TI - Instituto Tecnológico Cóndor).
Este documento sirve de evidencia para la **Sección 11 del Informe Final: Declaración de uso de IA** (herramientas utilizadas, uso específico y validación de aportes).

---

## Registro de Tareas

### Tarea: Fase 0 - Reglas y Preparación
- **Fecha:** 2026-11-20 18:14 (UTC-5)
- **Herramienta:** Antigravity (Gemini 3.8 Flash)
- **Solicitud del usuario:** 
  - Añadir a `.gitignore`: `.agent/`, `.gemini/`, `scratch/`.
  - Configurar las reglas permanentes del workspace del proyecto RAG (8 reglas: seguridad de credenciales, inmutabilidad de parámetros y preguntas/hipótesis tras congelación, control de llamadas a LLM, política de commits por el usuario, uso de `scratch/`, explicación pedagógica y bitácora de IA).
- **Qué generó / modificó:**
  - Actualización de `.gitignore` para ignorar `.agent/`, `.gemini/` y `scratch/`.
  - Creación de `AGENTS.md` en la raíz del proyecto y réplicas en `.agent/rules/AGENTS.md` y `.gemini/rules/AGENTS.md`.
  - Creación de las carpetas de trabajo `scratch/` e `informe/`.
  - Creación e inicialización de esta bitácora (`informe/bitacora_ia.md`).
- **Validación realizada:**
  - Verificación de sintaxis de `.gitignore` con `git status`.
  - Comprobación de que `.env` y claves permanecen protegidas y no tocadas.
  - Comprobación de que no se ejecutó ningún `git commit` ni `git push`.
  - Verificación de la lectura y coherencia con `README.md`, `PLAN_TRABAJO.md` y `Enunciado_Proyecto_RAG.md`.

---
