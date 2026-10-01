# OCI (Oracle Cloud) — línea base de costos (agosto y septiembre 2026)

| Versión | Fecha | Estado |
|---|---|---|
| 1.0 | 2026-10-01 | Medida con la CLI de OCI y una sesión temporal de Andres, solo lectura. Reemplaza al plan v0.1 |

Fuente: Usage API y consultas de solo lectura de la CLI (`oci`, sesión de navegador de una hora, sin llaves estáticas), región `us-ashburn-1`. Datos crudos en `datos/oci/` (no versionado); sin identificadores completos.

## Costo: USD 0,00 en agosto y en septiembre

Todo cabe en Always Free. La cuenta tiene límites de pago (el límite de núcleos de una forma de pago es 100, no 0), por lo que es **Pay As You Go con recursos Always Free** (verificar). Si algo excede lo gratuito, se cobra.

| Recurso | Uso de septiembre | Límite gratuito mensual | % |
|---|---|---|---|
| Cómputo A1, horas de OCPU | 1.440 | 1.500 | **96 %** (en agosto: 1.488, **99,2 %**) |
| Cómputo A1, GB-horas de memoria | 8.640 | 9.000 | **96 %** (en agosto: 8.928, **99,2 %**) |
| Block Volume (solo el disco de arranque) | 48 GB | 200 GB | 24 % |
| Object Storage, almacenamiento | 0,93 GB-mes (promedio) | 20 GB | 5 % (pero ver abajo) |
| Tráfico de salida | 6,8 GB | 10 TB | 0,07 % |

## Qué existe realmente

- **Una instancia** `VM.Standard.A1.Flex`, 2 OCPU y 12 GB, en marcha; **un disco de arranque de 50 GB; ningún volumen de bloque; ningún respaldo de volumen; ninguna IP reservada; ningún balanceador; un bucket**.
- **El hallazgo H-13 («150 GB de bloque sin usar») no existe en OCI.** No hay volúmenes sin adjuntar: se puede cerrar. El disco total es 50 GB de 200 gratuitos.

## Hallazgos

1. **Respaldos: la retención de 14 días no se aplica en el bucket.** `respaldos-proyectoa` tiene **520 objetos, 3,25 GiB, 41 días** (desde el 22/08); 328 objetos (0,63 GiB) tienen más de 14 días. El script declara `RETENCION_DIAS=14`, pero solo gobierna la copia local.
2. **El respaldo diario crece rápido:** de 183 MiB (27/09) a **326 MiB (1/10)**. **La base de datos de n8n es el 80 % del bucket** (2,6 GiB de 3,25). Refleja el crecimiento de las ejecuciones de NovuChat.
3. **Proyección:** a este ritmo y sin retención en el bucket, se alcanzaría el tope gratuito de 20 GB hacia mediados de noviembre. **El costo de pasarse es de centavos al mes** (tarifa de lista de Object Storage por verificar), no un monto relevante. **FinOps no propone borrar respaldos:** son un control de `docs/03` §1 (respaldos). Aplicar de verdad la retención que el propio script declara, o una regla de ciclo de vida, es **decisión del dueño** (WhatsApp-Modular y la sesión de n8n) y de Andres, con la prueba de restauración vigente.
4. **Cómputo al 96–99 % de lo gratuito:** la VM usa justo los 2 OCPU y 12 GB gratuitos. Cualquier OCPU, memoria o instancia extra se cobra. Hoy no hay margen para otra instancia.
5. **Riesgo de recuperación por inactividad (disponibilidad):** Oracle recupera una instancia Always Free si, durante 7 días, CPU (p95), red **y** memoria están por debajo del 20 %. Medido en los últimos 7 días: **CPU p95 7,5 %, red despreciable, memoria p95 21,5 %.** **La memoria está solo 1,5 puntos por encima del umbral:** hoy no se cumple la condición, pero **liberar memoria (por ejemplo, retirar los contenedores de laboratorio o limpiar Docker) podría dejar la VM en condición de ser recuperada**, y ahí corren Odoo y el OTP de SeguroLoTengo. Verificar si la política aplica a una cuenta Pay As You Go.

## Qué dice y qué no

- **No hay ahorro posible en OCI: ya cuesta cero.** El valor de esta línea base es vigilar tres umbrales: los 20 GB de Object Storage (mediados de noviembre), el tope de cómputo (sin margen) y la condición de inactividad (memoria al 21,5 %).
- **Un efecto contraintuitivo a tener presente:** optimizar el uso de memoria de la VM empeora el riesgo de recuperación. No se propone ninguna acción de limpieza sin hablar con los dueños.
- **La estimación de WhatsApp-Modular** (unos 170 MB de respaldos) era errónea por un factor de veinte: la retención no se aplica en el bucket. Ya se les comunica.

## Costo de la recolección
Usage API y consultas de la CLI: sin costo.

## Siguiente paso
Repetir el primer día hábil de cada mes. Vigilar el tamaño del bucket (umbral de aviso: 15 GiB) y la memoria de la VM. Cerrar H-13 en `n8n-oci` (decisión de esa sesión).
