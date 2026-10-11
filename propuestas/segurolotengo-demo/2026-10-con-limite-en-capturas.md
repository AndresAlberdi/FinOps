# Capturas con tope de memoria (`con-limite.sh`) — bloque para la sesión dueña de las capturas de SeguroLoTengo

> Origen: FinOps-Ecosistema, 2026-10-11. **Veredicto del guardián (2026-10-11): el bloque original iba dirigido a NovuChat
> (rechazado); esta versión corrige el dueño y las pruebas (N1 a N4). No se envía hasta que Andres diga que
> «SeguroLoTengo Sesion Principal» terminó: es la sesión dueña y no se toca antes.**
>
> Contexto: el 2026-10-10 entre las 02:39 y las 02:45 la memoria local (Playwright con `chrome-headless`, `next-server`,
> Chrome y la app de escritorio) agotó 32 GB y swap; el kernel mató GNOME Shell y con él la sesión. No fue cuota.
> Los scripts `c2-cap.sh` y `cap-c3.sh` existen (comprobado por nombre de archivo, sin abrirlos) en el espacio temporal
> de la sesión de `segurolotengo-demo` (worktree `seguro-lo-tengo-v5-analysis`), **sin versionar**; `segurolotengo-demo` es
> además el único proyecto con `next.config`. NovuChat y Novuchat-site no usan Next.

## Qué pedir
0. **Antes de nada:** llevar `c2-cap.sh` y `cap-c3.sh` a su repositorio, en una rama propia, con commit por ruta (están en un espacio temporal que se vacía al reiniciar).
1. Lanzar los comandos pesados de captura con el envoltorio de FinOps, **tanto el servidor como Playwright**, cada uno con su propio tope:
   `con-limite.sh -m 4G -- <next start …>` y `con-limite.sh -m 6G -- <playwright …>`.
   Copiar el script a su repositorio o fijar el commit `a40ca3d` de FinOps en lugar de depender de la rama que tenga sacada la carpeta principal de FinOps.
2. Correr las capturas contra `next build && next start`, **no** `next dev`. Al pasar a modo producción, confirmar que el build usa los mismos servicios no productivos que las capturas actuales (el modo producción cambia el comportamiento).
3. Playwright con **un solo worker**.

## Pruebas
- **Camino normal:** una captura normal termina bajo el tope y produce el **mismo número de imágenes** que sin él.
- **Caso malo, con red de seguridad:** antes de provocarlo, las demás sesiones con commit o su `ESTADO.md` al día y Andres avisado; empezar con un tope bajo; `earlyoom` ya está activo en el equipo (`-m 8,4 -s 20,10`, prefiere matar `chrome-headless` y `next-server`, protege `gnome-shell` y `claude`). Debe morir el script y no la sesión gráfica.

## Cómo usar el envoltorio
`con-limite.sh [-m TOPE] -- comando [argumentos…]` (TOPE entero con sufijo `M` o `G`; por defecto 6G; sin swap). Código de salida: el del comando; SIGKILL (137 en terminal) si superó el tope; 3 si no hay `systemd-run`. Probado por FinOps: 600 MB bajo un tope de 200 MB muere; 100 MB termina.

## Cómo trabajar
Worktree y rama propios; nunca `git add -A`; commit por ruta; push y PR solo con el «sí» de Andres en tu chat. Andres autoriza; tú operas.

## Controles de `docs/03` que toca
Ninguno. **Costo:** cero cuota de infraestructura, pero la sesión dueña gasta turnos en aplicarlo y probarlo (se declara y se mide). **Reversión:** dejar de anteponer el envoltorio.

## Lo que NO se pide
- No se modifica nada fuera de los scripts de captura.
- FinOps no edita archivos de `segurolotengo-demo`.
