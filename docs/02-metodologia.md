# 02 · Metodología

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-09-28 | Vigente |

Se sigue el ciclo del FinOps Framework (FinOps Foundation): **Informar → Optimizar → Operar**, en ciclos mensuales.

## 1. Ciclo de una palanca

1. **Línea base.** Costo real de los dos últimos ciclos de facturación completos y la métrica de calidad o servicio afectada (latencia, errores, calidad de respuesta, disponibilidad). Queda en `mediciones/<proveedor>/<AAAA-MM>-linea-base.md`.
2. **Propuesta** (`analista-finops`), con: palanca, ahorro esperado con su supuesto, riesgo, prueba de no regresión, reversión y proyecto dueño.
3. **Veredicto** (`guardian-calidad-seguridad`): APROBADA, APROBADA CON CONDICIONES o RECHAZADA, contra `03-guardarrailes.md`. Si toca identidades, IAM, redes o controles del pipeline, además el agente `seguridad`.
4. **Autorización** de Andres en el chat.
5. **Entrega** como bloque en `propuestas/<proyecto>/`; lo ejecuta la sesión dueña.
6. **Medición real** del ciclo siguiente frente a la línea base; si hay regresión, se revierte y se registra.

## 2. Priorización

Puntaje = ahorro mensual esperado × confianza ÷ (esfuerzo × riesgo). Se ejecutan primero las palancas de riesgo bajo y reversión inmediata, aunque el ahorro sea menor.

## 3. Catálogo inicial de palancas (a validar en cada caso)

| Dominio | Palanca | Riesgo típico | Prueba de no regresión |
|---|---|---|---|
| Claude | Modelo por rol en subagentes (Opus planifica y revisa; Sonnet ejecuta) — **ya aplicada el 2026-09-28** | Bajo | Tasa de PR rechazados por el revisor; retrabajo |
| Claude | `CLAUDE.md` estable y compacto para reutilizar la caché de prompts | Bajo | Mismas reglas presentes; tareas sin incidentes |
| Claude | Tope mensual de créditos de uso; paquetes con descuento solo con consumo estable | Bajo | Sesiones bloqueadas por límite |
| Claude / Gemini | Caché de prompts y Batch API (50 %) en cargas no interactivas vía API | Bajo | Mismas salidas en muestra de control |
| Nubes | Recursos huérfanos: discos, IP estáticas, instantáneas, buckets y proyectos sin uso | Bajo | Inventario confirmado con el dueño antes de borrar |
| Nubes | Ajuste de tamaño (*rightsizing*) con dos semanas de métricas | Medio | Latencia p95 y error, antes/después |
| Nubes | Apagado programado de entornos no productivos | Bajo | Horario acordado; arranque probado |
| Nubes | Ciclo de vida de almacenamiento y retención de logs **por encima** del mínimo normativo | Bajo | Retención mínima intacta |
| Nubes | Planes de ahorro o descuentos por compromiso, tras dos meses estables | Medio | Uso cubierto ≥ compromiso |
| n8n | Menos ejecuciones por evento (filtros tempranos, *debounce*, lotes) | Medio | Casos de prueba del flujo |
| Meta | Categoría correcta de plantilla y uso de ventanas de servicio gratuitas | Medio | Entregabilidad y tasa de respuesta |
| GitHub | Minutos de Actions: caché de dependencias, *path filters*, cancelar ejecuciones obsoletas | Bajo | Mismos controles del estándar corren |
| SaaS | Suscripciones duplicadas o sin uso | Bajo | Confirmación del titular |

## 4. Operación recurrente

Revisión mensual (primer día hábil): costo del ciclo cerrado frente al presupuesto por proveedor, anomalías (> 20 % sobre la media de tres meses), palancas en curso y mediciones pendientes. Se programa como tarea recurrente en el Bloque 4.
