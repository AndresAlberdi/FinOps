# Política de seguridad

Este repositorio (FinOps-Ecosistema) contiene documentación, propuestas, mediciones agregadas y scripts de consulta de solo lectura. No contiene secretos, datos de facturación detallados ni código de producción.

## Cómo reportar una vulnerabilidad

- **Vía principal:** abra un aviso privado en la pestaña **Security → Advisories → Report a vulnerability** de este repositorio.
- **Vía secundaria:** si no puede usar el aviso privado, abra un *issue* titulado «Seguridad: solicito contacto» **sin detalles técnicos ni datos sensibles**; la persona titular le indicará cómo enviar el detalle por el aviso privado.
- No publique secretos, claves ni identificadores completos de cuentas: si encuentra alguno en el historial, avise por la vía principal y no lo difunda.

## Plazos objetivo

- Acuse de recibo en **5 días hábiles** y decisión en **30 días** (corrección, descarte con motivo o mitigación). Ambos son plazos objetivo, sin garantía; los hallazgos críticos tienen prioridad.
- Una corrección pasa por un PR con revisión de seguridad y la aprobación de la persona titular del repositorio.

## Versiones soportadas

Solo la rama `main`.

## Hallazgos en copias del estándar

Los hallazgos en las copias de las plantillas del estándar de SeguridadGeneral (workflows y scripts) se reciben y se corrigen en la plantilla de origen, y luego se copian aquí. Solo se descartan con motivo los endurecimientos sin explotabilidad demostrada, por ejemplo `pip` con versión fija pero sin hash.
