# Publicación segura en Git

## 1. Inicializar

```bash
cd "/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Notion"
git init -b main
```

## 2. Verificar secretos y artefactos ignorados

```bash
git check-ignore -v public/apikey/key.txt
git check-ignore -v graphify-out/graph.json
git status --ignored
```

`key.txt`, `.env`, `.DS_Store` y `graphify-out/` deben aparecer como ignorados.

## 3. Preparar el primer commit

```bash
git add .
git status --short
git diff --cached --check
git ls-files public/apikey/key.txt
```

El último comando no debe producir salida. Revisa la lista completa antes de continuar.

```bash
git commit -m "feat: establish traceability system foundation"
git tag -a V1.0 -m "V1.0 - Initial traceability system foundation"
```

## 4. Crear el remoto

Crea un repositorio vacío, preferiblemente privado, sin README, licencia ni `.gitignore`
generados por el proveedor. Después enlázalo:

```bash
git remote add origin git@github.com:USUARIO/REPOSITORIO.git
git remote -v
git push -u origin main
git push origin V1.0
```

Si usas HTTPS, no guardes tokens en la URL; usa el gestor de credenciales del sistema.

## 5. Verificación final

Confirma en el remoto que no existen `public/apikey/`, `.env`, `graphify-out/` ni
archivos `.DS_Store`. Si un secreto llegara a publicarse, eliminar el archivo no basta:
se debe rotar la credencial y limpiar el historial.

Cada versión cerrada debe tener un tag anotado e inmutable. No muevas ni reutilices un
tag ya publicado; crea el siguiente número de versión.
