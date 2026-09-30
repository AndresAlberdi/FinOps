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

## Tarifas por región (Firestore Standard, USD, con fuente)

Fuente: Cloud Billing Catalog API, servicio Cloud Firestore (`services/EE2C-7FAC-5E08`), precios de lista en USD, consultada el 2026-09-30. Las páginas HTML de precios salen truncadas en las herramientas de esta sesión; el catálogo es la misma fuente oficial en forma de datos.

| Concepto | `nam5` (multirregional US) | `us-east1` (South Carolina) | `us-central1` (Iowa) |
|---|---|---|---|
| Almacenamiento, por GiB-mes | 0,18 | 0,18 | **0,15** |
| Lecturas, por 100 000 | 0,06 | 0,06 | **0,03** |
| Escrituras, por 100 000 | 0,18 | 0,18 | **0,09** |
| Borrados, por 100 000 | 0,02 | 0,02 | **0,01** |

**Hallazgo:** `nam5` y `us-east1` cuestan **lo mismo** en las cuatro filas. La multirregional no es más cara que `us-east1`; migrar de `nam5` a `us-east1` **no ahorra nada**. La región más barata es `us-central1`: −17 % en almacenamiento y −50 % en operaciones. Las tres regiones tienen cuota gratuita diaria por proyecto («with free tier» en el catálogo), por lo que en bases pequeñas la diferencia real es de centavos.

## Lo que no se sabe (y no se inventa)
- **Cuánto pagan hoy estas seis bases:** se sabrá con la facturación real. Migrar sobre precio de lista, sin medir, puede costar más en trabajo y riesgo que lo que ahorra.
- **Latencia y colocación:** elegir `us-central1` frente a `us-east1` depende de dónde estén las otras piezas (Functions, Cloud Run) de cada proyecto. No se evalúa aquí.

## Siguiente paso de FinOps
Medir el costo real de Firestore por proyecto con la exportación de facturación. Solo si alguna base cuesta de forma apreciable, proponer su migración al proyecto dueño, con prueba de no regresión y reversión (`docs/02` §1). Una base no cambia de región: mover exige base nueva y migración.
