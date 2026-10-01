# OCI (Oracle Cloud) — plan de línea base

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-10-01 | Plan; **sin acceso a OCI desde este equipo** (no hay CLI ni `~/.oci`). Cifras de costo: ninguna todavía |

## Qué hay (de `~/n8n-oci/00-estado-del-proyecto.md`, 23/08/2026, solo lectura)

Una sola instancia, `Odoo-Server-ProyectoA`, forma `VM.Standard.A1.Flex` (ARM): **2 OCPU, ~11,7 GiB de memoria, disco de arranque de 50 GB**. Corre en la misma máquina, en contenedores: Odoo con su PostgreSQL de otro producto en producción, el proxy Nginx Proxy Manager, el `otp-service` de WhatsApp-Modular (el OTP de SeguroLoTengo) y n8n de NovuChat (más tres contenedores de laboratorio en retiro). Los respaldos diarios van a Object Storage (12 MB por juego en agosto). El dominio es de DuckDNS (gratuito).

## Límites de Always Free (documentación oficial de Oracle, consultada el 2026-10-01)

| Recurso | Límite gratuito | Uso conocido |
|---|---|---|
| Cómputo ARM A1 | 2 OCPU y 12 GB | **2 OCPU y ~12 GB: en el tope** |
| Block Volume (arranque y bloque, suma) | **200 GB**; 5 respaldos | 50 GB de arranque + «unos 150 GB sin usar» (H-13 del diagnóstico) = **~200 GB: en el tope** |
| Object Storage | 20 GB y 50.000 solicitudes al mes | Respaldos de unos 12 MB por juego; hay que ver la retención |
| Tráfico de salida | 10 TB al mes | Muy por debajo |

## Hipótesis y qué la desmentiría

**Hipótesis: el costo de OCI es USD 0.** Todo cabe en Always Free, pero **dos recursos están exactamente en el tope**, así que cualquier crecimiento se cobra: un volumen o respaldo adicional, o una instancia extra, pasa a pago. La confirmación es Cost Analysis de OCI, que hoy nadie ha leído.

## Dos riesgos para decidir con los dueños (no son ahorros)

1. **«150 GB de block storage sin usar» (H-13, abierto):** si son volúmenes sin adjuntar, es un recurso huérfano. No cuesta mientras la suma no pase de 200 GB, pero **ocupa justo el margen**. Borrarlos exige confirmar con el dueño que no hay datos ni dependencias, y una copia previa si tienen datos (`docs/03` §2). No se propone borrar nada sin esa confirmación.
2. **Recuperación de instancias inactivas (disponibilidad, no costo):** Oracle recupera las instancias Always Free que, **durante 7 días seguidos, estén por debajo del 20 % en CPU (percentil 95), red y memoria** (esta última, solo para A1). La VM usaba unos 750 MiB de 11,65 GiB (≈6 % de memoria). **Si se cumple la condición, Oracle podría recuperarla,** y en ella corren producción de Odoo y el OTP de SeguroLoTengo. Verificar si la cuenta es Pay As You Go y si esa condición le aplica (verificar en la documentación de Oracle); no se propone ninguna acción hasta saberlo.

## Cómo se mide (de menor a mayor esfuerzo)

| Vía | Qué exige | Alcance |
|---|---|---|
| **A. Pantallas de la consola (Andres, unos 10 minutos)** | Nada nuevo: Facturación y administración de costos → **Análisis de costos** (septiembre, por servicio); Gobernanza → **Detalles de la tenencia** (tipo de cuenta); Almacenamiento → **Volúmenes de bloque** (lista de volúmenes y cuáles están sin adjuntar) | Confirma o desmiente la hipótesis de USD 0 y el hallazgo H-13 |
| B. CLI de OCI con sesión de navegador | Instalar `oci-cli` en un entorno virtual y que Andres inicie una sesión temporal (`oci session authenticate`, sin llaves estáticas) | Lecturas repetibles: uso y costo, volúmenes, buckets |
| C. Identidad dedicada de solo lectura | Grupo `finops-lectura` con permiso de lectura de informes de uso (`docs/04` §2.3) | Recolección mensual sin la cuenta de Andres; exige una escritura de IAM |

Recomendación: **A ahora** (basta una mirada); **B** solo si Cost Analysis muestra un cargo distinto de cero o si se quiere repetir mensualmente; **C** si la recolección se vuelve rutina.

## Coordinación
WhatsApp-Modular administra el `otp-service` en esa VM; se le preguntó (por mensaje) qué ve de OCI, el tipo de cuenta, el hallazgo H-13 y el tamaño del bucket de respaldos. No hay una sesión propia de `n8n-oci`.
