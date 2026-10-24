# Política de seguridad

Este repositorio (FinOps-Ecosistema) contiene documentación, propuestas, mediciones agregadas y scripts de consulta de solo lectura. No contiene secretos, datos de facturación detallados ni código de producción.

## Cómo reportar una vulnerabilidad

- **Preferido:** abra un aviso privado en la pestaña **Security → Advisories → Report a vulnerability** de este repositorio, cuando esté habilitado.
- **Mientras tanto:** abra un *issue* titulado «Seguridad: solicito contacto» **sin detalles técnicos ni datos sensibles**; la persona titular le responderá por un canal privado.
- No publique secretos, claves ni identificadores completos de cuentas: si encuentra alguno en el historial, avise por el canal anterior y no lo difunda.

## Qué se atiende y en qué plazo

- Se acusa recibo en un plazo objetivo de **5 días hábiles** y se informa la decisión (corrección, descarte con motivo o mitigación) en **30 días**, salvo hallazgos críticos, que se atienden primero.
- Una corrección pasa por un PR con revisión de seguridad y la aprobación de la persona titular del repositorio.

## Versiones soportadas

Solo la rama `main`.

## Qué no se considera vulnerabilidad

Hallazgos en copias de las plantillas del estándar de SeguridadGeneral (por ejemplo, instalaciones de pip sin hash): se corrigen en la plantilla de origen y se registra su descarte con motivo.
