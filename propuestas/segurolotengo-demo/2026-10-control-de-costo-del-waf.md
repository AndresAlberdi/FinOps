# Control de costo del firewall (WAF) de SeguroLoTengo: alertas de gasto e inventario — bloque para la sesión dueña de `segurolotengo-demo`

> Origen: FinOps-Ecosistema, 2026-10-25 (v2). **Veredictos: guardián, aprobada con condiciones G1 a G9; agente `seguridad`, aprobada con condiciones S1 a S9 (ambos del 2026-10-25, incorporados abajo). No se envía a la sesión dueña hasta que Andres lo autorice en el chat.**
>
> Contexto medido (Cost Explorer, USD, bruto; AWS marca octubre como estimado):
> - La facturación de AWS es **consolidada entre dos cuentas**: la demo (…8663) y producción (…7115). Octubre al 24/10: **35,29 en total, demo 23,37 y producción 11,92** (producción factura desde el 16/10). El presupuesto mensual `slt-demo-presupuesto-mensual` (tope 50) mostraba 35,29 gastados y 55,17 previstos en la lectura del 25/10.
> - Firewall (WAF + AmplifyWAF): ~0,72 por día del 12 al 16/10 y ~1,96 por día del 17 al 24/10 (meseta de 2,0 a 2,1; el 24 es parcial). Causa: el firewall de **producción**, nacido el 16/10.
> - Inventario verificado en vivo el 25/10 por las sesiones de SeguroLoTengo y de infraestructura de Bancard (solo lectura): **demo** 1 ACL (`slt-demo-web-acl`, 9 reglas aplicadas, 1 app de Amplify, asociación correcta); **producción** 1 ACL (`slt-prod-web-acl`, 19 reglas, 1 app y 1 rama). El costo es fijo, no depende del tráfico. Producción lo pidió Andres (cierre por IP, avisos de Bancard, límites), pero **su aprobación de costo del 16/10 fue solo para la demo**.
> - Con tarifas oficiales (aws.amazon.com/waf/pricing y docs.aws.amazon.com/amplify/latest/userguide/waf-pricing.html, consultadas el 2026-10-25): 5 USD por ACL y mes, 1 USD por regla y mes, 0,60 USD por millón de solicitudes y 15 USD por app de Amplify con firewall. Demo ≈ 29 al mes (5 + 9 + 15); producción ≈ 39 (5 + 19 + 15); total ≈ 68. Cada regla nueva suma ~0,03 por día.

## Qué pedir
0. **Inventario que falta (solo lectura, salida agregada):**
   - Por qué el código de `origin/main` define 12 reglas en la demo y hay 9 aplicadas (la bitácora registra 9 el 17/10): ¿qué estado manda? Partir siempre de `origin/main`, no del checkout local atrasado.
   - Confirmar que el ACL asociado a la app de la demo es `slt-demo-web-acl` con acción por defecto «block» (estado `ASSOCIATION_SUCCESS`) y que desde una IP ajena la respuesta es 403. Si el asociado es otro ACL fuera de IaC, es un hallazgo de seguridad y se escala antes de cualquier decisión de costo.
   - Origen de los recursos en CloudTrail (quién y cuándo) y, para el criterio de reglas, `AllowedRequests` y `BlockedRequests` por regla de los últimos 14 a 30 días.
   - **Formato de entrega: nombres, número de reglas, grupos administrados, fechas, asociación y si está en IaC. Sin IP, sin JSON completo del ACL ni de los IP sets, sin ARN ni identificadores de cuenta completos (solo los últimos dígitos).** Lo que exceda las lecturas que ya permite el rol de despliegue se lee con una identidad de solo lectura en sesión puntual y con el «sí» de Andres.
1. **Presupuestos de solo aviso del firewall, uno por cuenta:**
   - Demo (`infra/presupuesto.tf`): nombre con prefijo `slt-demo-` (la política solo admite `budget/slt-demo-*`), filtrado por el servicio `AWS WAF` más el tipo de uso `USE1-AmplifyWAF` (no por «AWS Amplify» completo, que incluye las compilaciones y no mide el firewall). Tope propuesto: 30 USD.
   - Producción (`infra/produccion/`, en la cuenta de producción): mismo filtro. Tope propuesto: 45 USD; **lo fija Andres** al aprobar el costo.
   - Avisos al 50 % y 80 % de lo gastado y al 100 % de lo proyectado, a la variable de correo que ya usan los presupuestos de la cuenta (`presupuesto_correo_alerta`, sin valor por defecto, en `.tfvars` no versionado). Correr siempre con ella cargada: sin ella el plan borra las alertas en silencio.
   - **Solo avisos.** Ningún `aws_budgets_budget_action` ni acción automática de IAM, SCP, apagado o desasociación sobre WAF o Amplify (fallaría abierto y no detiene el cobro fijo). Si se usa SNS, la política del tema se limita a `budgets.amazonaws.com` y `costalerts.amazonaws.com`, con `aws:SourceAccount` y sin suscripciones públicas.
2. **Aviso de anomalías (opcional; lo decide Andres):** la cuenta ya tiene el monitor por defecto de servicios de AWS y solo se permite uno de ese tipo, así que no se crea otro. Se pide una suscripción con umbral de **impacto total** de 5 USD (no «diario») sobre el monitor existente, o un monitor personalizado por cuenta vinculada. Limitación: el nivel actual ya es historial y no se detectará como anomalía; solo saltos futuros. Gratuidad del servicio: (verificar en la documentación oficial). **Exige permisos** que el rol de despliegue no tiene a propósito: Andres elige (a) ampliar el rol solo con `ce:CreateAnomalyMonitor`, `CreateAnomalySubscription`, `Get*`, `Update*`, `Delete*` y `TagResource` sobre los recursos de anomalías de la cuenta, versionado en el archivo de referencia de la política y revisado por `seguridad`, sin `ce:GetCostAndUsage` ni `ce:UpdateCostAllocationTagsStatus`; o (b) crearlo fuera de Terraform con una identidad de facturación. Si no elige, se queda solo con el punto 1.
3. **Decisión que NO es de este bloque:** si alguna regla del ACL ya no hace falta. El firewall de …8663 y el de …7115 son controles de `docs/03-guardarrailes.md` §1.4: reducir reglas, pasar la acción por defecto a «allow» o desasociar queda fuera de FinOps y se decide en la sesión dueña con revisión de `seguridad` y con la evidencia del punto 0. **Staging, pruebas y portada son ramas de la misma app y ya comparten el ACL**; «prescindir del firewall» no es admisible mientras haya `DEMO_MODE=true` o una rama procese cédulas y rostros reales. Compartir ACL entre apps solo se admite con acción por defecto «block», reglas acotadas por host y revisión de `seguridad`. Si el inventario encontrara un ACL o app huérfanos, retirarlos es limpieza, con confirmación del dueño, respaldo del JSON en el repositorio dueño (sin IP en FinOps) y revisión de `seguridad`.

## Pruebas (no regresión)
- **Plan acotado:** `terraform plan` y `apply` con `-target` solo sobre los recursos nuevos, desde el checkout con los `.tfvars`. Umbral: **«N por crear, 0 por cambiar, 0 por destruir»**; si toca cualquier otro recurso, se aborta. Plan adjunto al PR y mostrado a Andres antes del `apply`.
- **Protección intacta:** sin cambios en reglas, `default_action`, `visibility_config`, IP sets, asociación ni variables de entorno de la app; los presupuestos `slt-demo-presupuesto-mensual` e `slt-demo-presupuesto-identidad` quedan idénticos, con sus notificaciones.
- **La alerta funciona:** con el tope en un valor bajo de prueba llega el correo; se confirma y se restituye el tope real.
- **Costo:** lectura de Cost Explorer del 1/11 con octubre cerrado, por cuenta; el firewall se compara contra ~29 (demo) y ~39 (producción) al mes. Solo cuenta lo medido.

## Cómo trabajar
Worktree y rama propios, partiendo de `origin/main`; un PR por bloque; nunca `git add -A`; commit por ruta; **push y PR solo con el «sí» de Andres en tu chat**. Andres autoriza; tú operas. Nada en AWS sin su «sí» y sin el rol de despliegue de la sesión. Revisión del agente `seguridad` antes de cada OK de fusión. Ningún secreto, IP ni identificador completo en el repositorio.

## Controles de `docs/03` que toca
- §1.4 (WAF) y §1.7 (producción): solo se **inventarían**; no se reducen ni se modifican.
- §1.8 (monitoreo y alertas que protegen producción): se **refuerza**.
**Costo:** presupuestos de monitoreo sin acciones: 0 USD (página oficial de AWS Budgets, consultada el 2026-10-25); aviso de anomalías: (verificar); turnos de la sesión dueña: bajo. **Reversión:** `destroy -target` de los recursos nuevos (presupuestos y suscripción), que debe destruir solo lo nuevo; unos 5 minutos. La aplicación y la protección no cambian.

## Lo que NO se pide
- No se quitan ACL, reglas, grupos administrados ni la integración de Amplify; no se cambia la acción por defecto ni la asociación.
- **No se etiquetan** el ACL ni la app en este bloque: cambiaría esos recursos, arrastraría cambios pendientes de otras sesiones y no separaría ramas (el cobro es por ACL y por app, no por rama). Si se quisiera, va en un bloque aparte, con esquema `Project`/`Environment` existente y revisión de `seguridad`.
- No se amplía `finops-lectura` ni el rol de despliegue con comodines (`wafv2:*`, `Get*` sobre `*`, `ce:*`).
- No se cambia el tope de 50 USD del presupuesto general.
- FinOps no edita archivos de `segurolotengo-demo`.

## Fuera de este bloque (a evaluar aparte)
- Un chequeo externo que alerte si el ACL deja de estar asociado (hoy «nadie la vigila»): debe vivir en GitHub Actions, no en la laptop (política de Andres); lo propone la sesión dueña con `seguridad`.
- Qué sesión es dueña de `infra/produccion/`: la bitácora la atribuye a la «sesión de administración» y la lectura en vivo la hizo la sesión de infraestructura de Bancard. Confirmar antes de enviar.
