# Talk slide decks

Two decks, one set of shared images:

```
ai-builders/   the AI Builders deck (Democratising AI Platform Engineering with Open Source)
websummit/     the Web Summit deck
images/        logos, QR codes and photos used by both
fonts/         fonts used by both
```

## Services

| Service | What it does | Local port |
|---|---|---|
| `ai-builders` | nginx serving the AI Builders deck at `/` | 8080 |
| `websummit` | nginx serving the Web Summit deck at `/` | 8081 |
| `cloudflared` | Cloudflare Tunnel to whichever deck is running (optional, profile `tunnel`) | none |

Both deck services also answer on the Docker network under the alias `deck` (port 8080),
which is what the tunnel points at. Run **one deck at a time** when using the tunnel.

## Run it

Start the deck you want:

```bash
docker compose up -d --build ai-builders
```

```bash
docker compose up -d --build websummit
```

Open <http://localhost:8080> (AI Builders) or <http://localhost:8081> (Web Summit).
Locally you can run both at once.

Stop everything with `docker compose down`.

## Reach it through your Cloudflare tunnel

One-time setup:

1. `cp .env.example .env` and paste your tunnel token into `TUNNEL_TOKEN`.
2. In Cloudflare Zero Trust, open the tunnel, add a **Public hostname**, and set its
   service to `HTTP` and `deck:8080`.

Expose a deck:

```bash
docker compose --profile tunnel up -d --build ai-builders cloudflared
```

### Switch the exposed deck

Stop the current deck, then start the other. The tunnel keeps running and picks up the new one
under the same `deck` alias, so the public URL doesn't change.

```bash
docker compose stop ai-builders
```

```bash
docker compose up -d --build websummit
```

To switch back, stop `websummit` and start `ai-builders` again.

If you already run `cloudflared` on the host, skip the steps above and point the hostname at
`http://localhost:8080` (AI Builders) or `http://localhost:8081` (Web Summit); change the hostname's
service in Cloudflare to switch.
