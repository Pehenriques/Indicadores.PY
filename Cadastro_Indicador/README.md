# Cadastro de Indicadores - Flask + MySQL

Este projeto é um sistema web de cadastro e gerenciamento de indicadores com front-end HTML, API Flask e persistência em banco MySQL.

## Como rodar localmente

```bash
pip install -r requirements.txt
python app.py
```

## Deploy no Render

- Suba este projeto para um repositório GitHub
- Configure variáveis de ambiente no Render:
  - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- Render detectará `render.yaml` automaticamente
- Use `Free Plan` se quiser custo zero

## Requisitos atendidos

- [x] API REST com múltiplos endpoints
- [x] Persistência com MySQL
- [x] Front-end com Jinja2/HTML
- [x] Deploy PaaS via Render
- [x] Código limpo e organizado
