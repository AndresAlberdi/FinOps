# 03 · Guardarraíles: lo que el ahorro no toca

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-09-28 | Vigente. Cambios solo por PR con revisión del agente `seguridad` |

## 1. Controles que nunca se proponen como ahorro

1. Cifrado en reposo y en tránsito; KMS y Secret Manager.
2. Respaldos, versionado de buckets con datos de negocio y objetivos RTO/RPO documentados (`~/SeguridadGeneral/01-seguridad/06-rollback-e-incidentes.md`).
3. Retención de logs, auditoría y evidencias **exigida por norma o contrato** (por ejemplo, conservación de SeguroLoTengo y actas de firma). Solo se optimiza lo que supera ese mínimo.
4. WAF, App Check, rate limiting y cabeceras de seguridad.
5. Los controles del pipeline del estándar DevSecOps v2 (Semgrep, Gitleaks, Trivy, OSV, Checkov, ZAP, CodeQL) y las licencias GHAS en modo B.
6. Federación OIDC/WIF: nunca se reemplaza por claves estáticas para ahorrar complejidad o costo.
7. Alta disponibilidad y redundancia de producción declaradas (por ejemplo, los tres nodos de firma F2).
8. Monitoreo y alertas que protegen producción.
9. La calidad de modelo en tareas de planificación, revisión y seguridad: bajar de modelo solo en ejecución de planes ya definidos.

## 2. Condiciones de toda propuesta

- Prueba de no regresión definida **antes** del cambio, con su métrica y umbral.
- Reversión documentada y probada, con su tiempo estimado.
- Proyecto dueño identificado; la ejecución es de su sesión.
- Si toca identidades, IAM, redes, retención o el pipeline: revisión del agente `seguridad`.
- Borrado de recursos: solo tras confirmar con el dueño que no hay dependencias, y con respaldo o instantánea previa cuando contengan datos.

## 3. Accesos de este proyecto

Solo lectura de facturación y configuración (`04-accesos.md`). Cualquier permiso de escritura que se solicite para este proyecto es, por definición, un error de diseño y se rechaza.
