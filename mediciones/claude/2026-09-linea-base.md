# Claude — línea base de cuota (palanca: modelo por rol)

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-09-29 | Método y primer dato; la serie se completa semanalmente |

## 1. Qué se mide y por qué así

La cuenta usa el **plan Pro** (no Max, como suponían `docs/00` §2 y `docs/01` §1; corregir en el Bloque 1). En un plan de suscripción el costo en USD es fijo; lo que la palanca reduce es el **consumo de cuota**: porcentaje de la ventana semanal «todos los modelos» y de la de Fable, y las veces que se toca el límite. El ahorro se expresa como: menos cuota por unidad de trabajo, o la misma cuota para más trabajo, sin regresión de calidad.

## 2. Fuente y método (reproducible)

1. **Fuente:** la herramienta `get_usage` de la app de escritorio de Claude Code (lectura; misma cifra que la tarjeta de uso de la app). Devuelve, por ventana, `% usado` y hora de renovación. No da historia: solo el valor del momento.
2. **Frecuencia:** una lectura al cierre de cada jornada y una **justo antes de cada renovación semanal** (la ventana actual vence el 2026-10-02 08:00 UTC). La lectura previa a la renovación es el dato de la semana.
3. **Unidad de trabajo (normalización):** PR fusionados en la semana en los seis proyectos prioritarios, más sesiones principales activas. Se toma de GitHub (solo lectura) y de la lista de sesiones de la app.
4. **Indicador:** `% semanal usado ÷ PR fusionados` y número de veces que se alcanzó un límite (5 h o semanal).
5. **Comparación:** semana del 25/09 al 02/10 (mezcla: la v1 rige desde el 28/09) frente a la semana del 02/10 al 09/10 (v1 completa) y la siguiente a la fecha en que Andres fije la sesión principal en Sonnet (v2-A).
6. **No regresión (quién la vigila):** PR con defectos hallados por `revisor-codigo` después de la fusión y retrabajo; lo reporta cada sesión en su `ESTADO.md` §«Coordinación», fila «Costo».

## 3. Serie

| Fecha y hora (UTC) | Ventana 5 h | Semanal, todos los modelos | Semanal, Fable | Uso extra | Nota |
|---|---|---|---|---|---|
| 2026-09-29 13:44 | 12 % | **84 %** | 73 % | desactivado (tope USD 40) | Faltan 2 d 18 h para renovar; 6 sesiones prioritarias activas en paralelo |

## 4. Límites de esta línea base

- **Antes del 28/09 no hay serie:** la herramienta no da historia. Si Andres quiere un punto previo, se puede leer su captura de claude.ai → Settings → Usage (verificar si muestra semanas anteriores). No se usan los transcripts de `~/.claude/projects`, que las reglas de Andres dejan fuera.
- El 84 % con más de dos días por delante indica que **esta semana la cuota es la restricción real**; la jornada paralela de hoy la consume más rápido. La cifra de la semana 25/09–02/10 no es representativa del uso normal.
- La comparación es de cuota, no de USD: el ahorro en USD solo existe si se evita activar el uso extra o subir de plan.
