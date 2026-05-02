# vertere

[TODO: Describe the project]

## Getting Started

1. Ensure shared infrastructure is running: `cd ~/dev/infra && podman compose up -d`
2. Copy `.env.example` to `.env.local` and fill in secrets
3. `direnv allow`
4. `deno task dev`

## Mobile / webhook testing

Public URL via the shared cloudflared tunnel. Add this to
`/etc/cloudflared/config.yml` and route the DNS:

```yaml
ingress:
  - hostname: verteredev.noregrets.dev   # internal
    service: http://localhost:8787
```

```bash
cloudflared tunnel route dns <tunnel-id> verteredev.noregrets.dev
sudo systemctl restart cloudflared
```

Then `https://verteredev.noregrets.dev` reaches your local API.

## Docs

- [`CLAUDE.md`](./CLAUDE.md) — AI context and conventions
- [`docs/`](./docs/) — detailed documentation
