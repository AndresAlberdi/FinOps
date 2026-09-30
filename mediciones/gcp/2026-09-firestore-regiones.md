# Firestore: región por proyecto (cuenta principal de Google)

| Versión | Fecha | Fuente |
|---|---|---|
| 0.1 | 2026-09-30 | `gcloud firestore databases list` de solo lectura, con la cuenta principal de Google, sobre los 26 proyectos que ve. Datos crudos en `datos/gcp/` (no versionado) |

Preferencia de Andres: `us-east1`, una sola región, sin multirregión. La región de una base de Firestore **no se cambia** una vez creada: moverla exige una base nueva y migrar los datos.

| Región | Proyectos | Nota |
|---|---|---|
| **`nam5` (multirregional US)** | `demob-1e4a1`, `hipatia-puntos`, `pretso-database`, `pretso-prod`, `snack-laestacion`, `whatsappmodular` | Seis bases. `pretso-prod` está vacía según el plan de migración de PRETSO |
| `us-central1` | `encuentramebo-1`, `puntosnb` | `encuentramebo-1` por diseño (latencia con Vertex AI) |
| `us-east1` (preferida) | `aab1-receptor`, `novuchat-demo`, `novuchat-site`, `novuchatstaging`, `pruebas-mj`, `demoa-c585c` | `demoa-c585c` figura «a borrar» en el inventario de SeguridadGeneral |
| Sin Firestore (API apagada) | 14 proyectos | Nada que hacer |

Aclaración sobre WhatsApp-Modular: sus documentos no se contradicen; hay dos proyectos. El receptor de clientes vive en `aab1-receptor` (`us-east1`) y el conector en `whatsappmodular` (`nam5`).

## Lo que no se sabe (y no se inventa)
- **Tarifa por región de Firestore:** las páginas oficiales salen truncadas en las herramientas de esta sesión y no se pudo citar la diferencia (verificar en https://cloud.google.com/firestore/pricing, «Standard edition»).
- **Cuánto pagan hoy estas seis bases:** se sabrá con la facturación real. Con volúmenes pequeños, la cuota gratuita diaria y el almacenamiento mínimo suelen dejar la diferencia en centavos; migrar sobre precio de lista, sin medir, puede costar más en trabajo y riesgo que lo que ahorra.

## Siguiente paso de FinOps
Medir el costo real de Firestore por proyecto con la exportación de facturación. Solo si alguna base multirregional cuesta de forma apreciable, proponer su migración al proyecto dueño, con prueba de no regresión y reversión (`docs/02` §1).
