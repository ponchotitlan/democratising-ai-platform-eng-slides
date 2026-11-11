# Talk slide decks

Two decks, one set of shared images:

```
ai-builders/   the AI Builders deck (Democratising AI Platform Engineering with Open Source)
websummit/     the Web Summit deck
images/        logos, QR codes and photos used by both
fonts/         fonts used by both
```

## Services

| Service | What it does | Port |
|---|---|---|
| `caipe-ai-builders` | nginx serving both decks: `/` (AI Builders) and `/websummit/` | 8080 |
| `cloudflared` | Cloudflare Tunnel to the deck (optional, profile `tunnel`) | none |

## Run it

```bash
docker compose up -d --build
```

Open <http://localhost:8080> (AI Builders) or <http://localhost:8080/websummit/> (Web Summit).
Stop it with `docker compose down`.

## Reach it through your Cloudflare tunnel

1. `cp .env.example .env` and paste your tunnel token into `TUNNEL_TOKEN`.
2. In Cloudflare Zero Trust, open the tunnel, add a **Public hostname**, and set its
   service to `HTTP` and `caipe-ai-builders:8080`.
3. Start both services:

```bash
docker compose --profile tunnel up -d --build
```

If you already run `cloudflared` on the host, skip the steps above and point the
hostname at `http://localhost:8080`.
