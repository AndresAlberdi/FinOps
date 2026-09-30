# Claude — línea base de cuota (palanca: modelo por rol)

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-09-29 | Método y primer dato; la serie se completa semanalmente |

## 1. Qué se mide y por qué así

`get_usage` reportó **plan Pro** el 2026-09-29 y **plan Max** el 2026-09-30 (ver §3): el plan cambió entre ambas lecturas (créditos o mejora de plan, según Andres, condiciones de Claude: consumir en 40 horas el equivalente a una semana). `docs/00` §2 y `docs/01` §1 dicen Max, lo cual vuelve a coincidir; no hay nada que corregir por ahora. En un plan de suscripción el costo en USD es fijo; lo que la palanca reduce es el **consumo de cuota**: porcentaje de la ventana semanal «todos los modelos» y de la de Fable, y las veces que se toca el límite. El ahorro se expresa como: menos cuota por unidad de trabajo, o la misma cuota para más trabajo, sin regresión de calidad.

## 2. Fuente y método (reproducible)

1. **Fuente:** la herramienta `get_usage` de la app de escritorio de Claude Code (lectura; misma cifra que la tarjeta de uso de la app). Devuelve, por ventana, `% usado` y hora de renovación. No da historia: solo el valor del momento.
2. **Frecuencia:** una lectura al cierre de cada jornada y una **justo antes de cada renovación semanal** (la ventana actual vence el 2026-10-02 08:00 UTC). La lectura previa a la renovación es el dato de la semana.
3. **Unidad de trabajo (normalización):** PR fusionados en la semana en los seis proyectos prioritarios, más sesiones principales activas. Se toma de GitHub (solo lectura) y de la lista de sesiones de la app.
4. **Indicador:** `% semanal usado ÷ PR fusionados` y número de veces que se alcanzó un límite (5 h o semanal).
5. **Comparación:** semana del 25/09 al 02/10 (mezcla: la v1 rige desde el 28/09) frente a la semana del 02/10 al 09/10 (v1 completa) y la siguiente a la fecha en que Andres fije la sesión principal en Sonnet (v2-A).
6. **No regresión (quién la vigila):** PR con defectos hallados por `revisor-codigo` después de la fusión y retrabajo; lo reporta cada sesión en su `ESTADO.md` §«Coordinación», fila «Costo».

7. **Palanca A (sesión principal en Sonnet): se mide por observación, no por configuración.** Según SeguridadGeneral (2026-09-29), `/model <nombre>` guarda el valor por defecto en la CLI, pero en la app de escritorio no se observó ese guardado (`~/.claude/settings.json` sin clave `model` tras un `/model sonnet`). **Fecha de inicio de A: 2026-09-29**, confirmada por Andres (una sesión nueva arrancó en Sonnet). El mecanismo no es `~/.claude/settings.json` (sin clave `model`, sin cambios desde 2026-09-25); no se sabe si es un ajuste de la app o el efecto de `/model`. Por eso, en cada lectura se anota el modelo con que arrancó cada sesión principal abierta ese día.
8. **Tarifas de referencia** (claude.com/pricing, consultadas por SeguridadGeneral el 2026-09-29; matriz §9 de SeguridadGeneral): Haiku 4.5, USD 1/5 por millón de tokens de entrada y salida, lectura de caché USD 0,10; la página ya nombra «Sonnet 5.5» (verificar si cambia la tarifa de Sonnet antes de usarla).

## 3. Serie

| Fecha y hora (UTC) | Ventana 5 h | Semanal, todos los modelos | Semanal, Fable | Uso extra | Nota |
|---|---|---|---|---|---|
| 2026-09-29 13:44 | 12 % | **84 %** | 73 % | desactivado (tope USD 40) | Plan: Pro. Faltan 2 d 18 h para renovar; 6 sesiones prioritarias activas en paralelo |
| 2026-09-30 18:57 | 14 % | **4 %** | 0 % | desactivado (tope USD 40) | Plan: **Max**. Renueva 2026-10-02 08:00 UTC. La ventana semanal se reinició con los créditos; condición de Andres: consumir el equivalente a 1 semana en 40 h |

## 4. Límites de esta línea base

- **Antes del 28/09 no hay serie:** la herramienta no da historia. Si Andres quiere un punto previo, se puede leer su captura de claude.ai → Settings → Usage (verificar si muestra semanas anteriores). No se usan los transcripts de `~/.claude/projects`, que las reglas de Andres dejan fuera.
- El 84 % con más de dos días por delante indica que **esta semana la cuota es la restricción real**; la jornada paralela de hoy la consume más rápido. La cifra de la semana 25/09–02/10 no es representativa del uso normal.
- La comparación es de cuota, no de USD: el ahorro en USD solo existe si se evita activar el uso extra o subir de plan.

## 5. Verificación del modelo de arranque (2026-09-29, ~15:25 UTC)

Fuente: `get_session` (metadatos; no lee conversaciones). **El campo `model` es el modelo actual de la sesión, no el de arranque.** No hay historial de cambios.

| Sesión | Creada (UTC) | Modelo ahora | Lectura |
|---|---|---|---|
| FinOps (esta) | 09-29 02:42 | sonnet-5-5 | Arrancó en **Opus**; pasó a Sonnet por `/model` de Andres |
| NovuChat · Análisis financiero | 09-29 02:34 | sonnet-5-5 | Única creada hoy que está en Sonnet; no se sabe si arrancó así |
| SeguroLoTengo · Confirmar modelo por rol | 09-29 12:28 | **opus-5-5** | Creada por otra sesión (`parentSessionId`), no abierta por Andres |
| NovuChat · Constructora/Operadora | 09-25 20:33 | **opus-5-5** | Inactiva desde 05:39 UTC; no se reinició |
| SeguridadGeneral, Claude-Proyectos, SeguroLoTengo, PRETSO, WhatsApp-Modular, NovuChat (principal y cartera) | 08-19 a 09-27 | sonnet-5-5 | Creadas antes de hoy: cambiadas después de crearse, no «arrancaron» en Sonnet |

**Conclusión: no confirmada.** Ninguna sesión creada por Andres después de su prueba (~15:00 UTC) existe todavía, así que no hay caso limpio. Las sesiones antiguas en Sonnet fueron cambiadas; dos siguen en Opus. Los datos son compatibles con «se cambiaron a mano» tanto como con «arrancan en Sonnet».

**Prueba limpia pendiente:** Andres abre una sesión nueva desde el botón de la app (sin escribir `/model`) y FinOps lee su `model` con `get_session` de inmediato. Si dice `claude-sonnet-5-5`, A queda confirmada con esa hora.

**Cuota por modelo:** `get_usage` no separa por modelo salvo la ventana «Weekly · Fable» (73 %, no se sabe qué modelos incluye); no permite fijar desde qué hora cambió el consumo.

## 6. Ventana de 40 horas (desde 2026-09-30)

Andres consiguió créditos con la condición de consumir el equivalente a una semana en 40 horas. La comparación semanal del §2 pierde sentido mientras dure: la unidad pasa a ser la **ventana de 40 h**. Se anota el `% semanal` al inicio y al fin, las horas reales y los PR fusionados en ese lapso. Inicio de la ventana: 2026-09-30 ~19:00 UTC (4 % usado). Fin: a las 40 h de trabajo efectivo o al agotarse el crédito, lo que ocurra antes (la fecha exacta la confirma Andres; verificar en las condiciones de Claude).
