# Robot Server - Flask

Servidor básico para simular la comunicación entre dos robots usando Flask.

## Endpoints

- `POST /send/a` — Robot A envía mensaje a B
- `POST /send/b` — Robot B envía mensaje a A
- `GET /receive/a` — Robot A recibe mensaje de B
- `GET /receive/b` — Robot B recibe mensaje de A

## Ejemplo

```bash
curl -X POST https://<tu-url>.onrender.com/send/a -H "Content-Type: application/json" -d '{"message":"Hola B"}'
curl https://<tu-url>.onrender.com/receive/b
