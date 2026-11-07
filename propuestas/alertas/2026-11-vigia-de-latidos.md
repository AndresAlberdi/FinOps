# Diseño: vigía de latidos de FinOps (2026-11-07)

Estado: DISEÑO. Nada construido. Cada escritura la autoriza Andres. Dueño: FinOps. Responde al punto 3 de la revisión de SeguridadGeneral (anexo 15, AL-09) y a la política del 11/10 (silencio = alerta).

## Qué hace
Una vez al día revisa que cada alerta o monitor programado de los proyectos siga vivo (que su último workflow exitoso sea reciente) y envía UN solo correo-resumen. Cuesta 1 de los 50 envíos diarios compartidos (decisión D-4). Si algún latido falta, el mismo correo lo dice y sube a nivel «urgente».

## Dónde corre
Workflow programado en el repositorio `AndresAlberdi/FinOps` (público), 12:30 UTC, después del resumen de WAM de las 12:00. Environment dedicado `vigia-latidos`, limitado a `main`. No depende de la laptop.

## Qué lee (solo lectura)
- Archivo versionado `vigia/latidos.yml`: lista cerrada de entradas (proyecto, repositorio, archivo del workflow, edad máxima en horas). Agregar un proyecto es un PR revisado.
- Por entrada, la API de GitHub Actions: conclusión y fecha del último run del workflow indicado. Nada más (ni títulos, ramas, commits ni logs).

## Correo (contrato `avisos-correo/v1`)
- Texto armado SOLO con enumeraciones, números y fechas: nombre del proyecto (de la lista cerrada), estado (`vivo|atrasado|fallido|sin_datos`), horas desde el último éxito. Nunca se copia un título de run, rama, commit, mensaje ni respuesta de la API (Seguridad AL-09).
- Remitente `alertas-finops@avisos.aab1.website`. `Idempotency-Key` y `id_unico` = `vigia-AAAA-MM-DD` (sin racha de 7 dígitos; sigue abierta con WAM la regla de los detectores).
- Nivel `informativo` si todo vive; `urgente` si hay alguno atrasado, fallido o sin datos. Lo esencial en los primeros 400 caracteres.
- Sin enlaces a datos de terceros: solo al panel público de Actions de FinOps.

## Credenciales (clase S2, rotación ≤ 180 días)
| Qué | Decisión |
|---|---|
| Lectura de Actions | GitHub App de solo lectura (Actions: read, Metadata) instalada en los repositorios listados. Preferida por Seguridad |
| Alternativa | Token fine-grained con repositorios explícitos y vencimiento ≤ 180 días. **Un token cubre un solo propietario**: los repositorios están bajo dos cuentas (AndresAlberdi y segurolotengopy), así que serían dos tokens o una App instalada en ambas |
| Clave de Resend | Propia de `alertas-finops`, solo envío, limitada al dominio, como secreto del Environment |
| Salida pública | El repositorio es público: el registro imprime solo «OK/ATRASADO» por entrada y el total; sin montos, sin ids, sin respuestas crudas; errores descartados |

## Latido de la propia vigía (no depende de que Andres note la falta del correo)
1. Al terminar bien, hace ping a un check de Healthchecks.io (URL como secreto). Gracia de 26 h. Si no llega, Healthchecks avisa a Andres por correo, por un canal ajeno a Resend y a GitHub.
2. Si el workflow falla, llega el correo de fallo de GitHub.
3. Si ambos callan, queda el cierre mensual como revisión manual (último recurso, no la defensa principal).
Con esto el silencio de la vigía también alerta (monitor de latido del monitor).

## Límites y costo (verificar con fuente y fecha antes de construir)
- Costo: 0 USD. Repositorio público = Actions gratis; Resend dentro del cupo (1/día); Healthchecks Hobbyist (20 trabajos; que el correo esté incluido: verificar).
- Los workflows programados se desactivan tras 60 días sin actividad en el repositorio (verificar): el propio latido lo detecta.
- Máximo de claves de Resend por plan: sin verificar.

## Prueba de no regresión y reversión
- Prueba: con la entrada de un workflow que se sabe vivo (OCI, tras su primera corrida) y otra con edad máxima artificialmente baja; confirmar correo `urgente` y luego normal. Detener el ping a propósito y confirmar el aviso de Healthchecks en ≤ 27 h.
- Reversión: desactivar el workflow, borrar el Environment, la App o el token, la clave de Resend y el check.

## Qué NO se hace
- No lee contenido de logs ni artefactos de otros repositorios.
- No corre en la VM de OCI ni depende de n8n.
- No usa token con escritura ni acceso a toda la cuenta.
- No envía un correo por entrada: uno solo, agrupado.

## Pasos, quién y autorización
| Paso | Quién | Autoriza Andres |
|---|---|---|
| PR con `vigia/latidos.yml`, workflow y script (borrador, revisor de código + seguridad) | FinOps | OK al PR |
| Crear la GitHub App (o los tokens) e instalarla en los repositorios | Andres (lo exige a una persona) | Sí |
| Crear Environment, secretos (App, clave Resend, URL de ping) | FinOps, con OK | Sí |
| Crear la clave de Resend de `alertas-finops` | Andres en el panel | Sí |
| Crear el check de Healthchecks | Andres (cuenta) | Sí |
| Anotar la clave y el token en el inventario de secretos (sin valores) | FinOps / Seguridad | Sí |

## Dependencias
Contrato y detectores de WAM (ADR-011); anexo 15 de Seguridad (AL-09); la primera corrida real de OCI (PR 42) como primera entrada viva.

## Desviaciones del diseño en la implementación (revisión de código y de seguridad, 2026-11-07)
- **Archivo de configuración:** `vigia/latidos.json`, no `.yml` (solo biblioteca estándar). El script vive en `vigia/`, no en `scripts/`, porque envía correo y `scripts/` es de solo lectura por invariante.
- **Identidad del aviso:** `id_unico` = `vigia-AAAA-MM-DD-HHMM` y `ocurrido_en` al minuto, no la clave por día: con la clave por día, un relanzamiento el mismo día recibía un 409 de Resend por carga distinta y no enviaba. Los reintentos de una corrida llevan la misma clave y los mismos bytes. Costo: un relanzamiento manual consume un envío de la reserva.
- **Estado:** horas desde el último ÉXITO (consulta `status=success`); «fallido» solo si el último run completado falló y es posterior al éxito; `cancelled`, `skipped` y `neutral` se ignoran.
- **Registro público:** una línea JSON con totales (`vivos`, `total`), sin estado por entrada: lo exige la regla de no filtrar datos de terceros; el detalle va en el correo.
- **Validador:** mínimo (prefijos de secretos, IPv4, `localhost`, `.internal`, `.local`, largos, campos fijos), no el espejo completo del corpus de WAM. Se declara en la ficha, como la receta curl.
- **Errores de Resend:** solo se lee el campo enumerado `name`. 409 concurrente y 429 de frecuencia se reintentan; cuota agotada sale con 12; el resto de los 4xx sale con 13 sin reintento. Los 3xx no se siguen (el token nunca viaja a otro destino).
- **Remitente:** debe ser `alertas-finops@…`; nombre visible «AAB1 avisos · finops».
- **Presupuesto de tiempo:** 240 s para consultar a GitHub; el resto pasa a «sin datos». El trabajo tiene 8 minutos.

## Requisito antes de cargar secretos (Seguridad, MEDIUM)
Crear el Environment `vigia-latidos` con política de ramas limitada a `main` y verificarla ANTES de cargar los secretos; después, fusionar el workflow.

## Primera entrada
`wam`: repositorio de WAM, workflow del latido del receptor (cron cada 6 h, leído en solo lectura el 07/11), máximo 14 h.
