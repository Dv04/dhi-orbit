# Contributing to DHI Orbit

Bug reports, ideas and pull requests are welcome. Questions: [Discussions](https://github.com/Dv04/dhi-orbit/discussions).

## Run it from a checkout

```sh
git clone https://github.com/Dv04/dhi-orbit && cd dhi-orbit
python3 -m venv .venv && .venv/bin/pip install pytest markdown
.venv/bin/python -m pytest -q          # full suite
python3 tools/mock/server.py           # the UI on synthetic data: http://127.0.0.1:8791/v2/?token=mock
```

`tools/mock/server.py` never reads real chats. `tools/acceptance/` holds the browser checks (Chrome DevTools protocol, no extra packages).

## Pull requests

- One change per PR. A bug fix comes with a test that fails without it.
- The runtime stays Python standard library only (Windows adds `pywinpty` and `tzdata`); no build step, no CDN.
- Keep the public tree free of private paths and company names (`tests/test_no_company_refs.py` checks it).
- Run the tests that cover what you changed before you push; the full suite runs once the PR is ready.

New agent support is the most useful contribution: the provider layer lives in `dhi_orbit/providers`, and an agent you cannot add as code can often be described in `agents.json` (see the README).
