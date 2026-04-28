# SubSonic-Festival-FrontEnd
El FrontEnd de la aplicación SubSonic Festival

## Sincronizar JSON -> JS por vista

Para mantener sincronizados los archivos `*-data.json` y `*-data.js`, usa:

```powershell
./sync-data-files.ps1
```

También puedes ejecutar directamente:

```bat
sync-data-files.cmd
```

Este proceso recorre todos los `*-data.json` del proyecto y genera su `*-data.js` equivalente con el formato:

```javascript
window.NOMBRE_DATA = { ... }
```
