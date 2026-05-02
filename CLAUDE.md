# vertere — AI Context

**Read this first.** Every AI session on this project starts here.

## What This Is

[TODO: One paragraph describing the product.]

## Architecture

- **Runtime:** Deno 2.x
- **Framework:** Hono
- **Language:** TypeScript strict mode
- **Database:** PostgreSQL via postgres.js + Drizzle
- **Deployment:** Azure Container Apps

## Conventions

- TypeScript strict — no `any` except FFI boundaries
- Tagged template SQL via `postgres` driver
- Zod validation at every input boundary
- Handlers pure, routes thin
- Commit format: `scope: action`

## Running

```bash
# Infrastructure (shared, should already be running)
cd ~/dev/infra && podman compose up -d

# This project
deno task dev
```

## Mobile / webhook testing (cloudflared)

The shared cloudflared service runs as systemd
(`/etc/cloudflared/config.yml`). Add a new ingress rule:

```yaml
ingress:
  - hostname: verteredev.noregrets.dev   # or vertere.certopartners.com for clients
    service: http://localhost:8787
```

Then route the DNS:

```bash
cloudflared tunnel route dns <tunnel-id> verteredev.noregrets.dev
sudo systemctl restart cloudflared
```

For Expo Go on a phone, also tunnel Metro (`http://localhost:8081`) under
a second hostname (e.g. `verteremetro.noregrets.dev`) and start with
`EXPO_PACKAGER_PROXY_URL` + `REACT_NATIVE_PACKAGER_HOSTNAME` pointing at it.

## Where to Look

- `README.md` — getting started
- `docs/` — deeper documentation
- `packages/schemas/` — data shapes

## Current Status

[TODO: What phase / what's in progress]
