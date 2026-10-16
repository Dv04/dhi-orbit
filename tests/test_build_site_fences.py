"""The docs page must render a fenced block inside a list item as <pre><code>, with its indentation kept and no language tag in the text."""
import os
import sys

import pytest

pytest.importorskip("markdown")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
from mdrender import render  # noqa: E402

DOC = """1. Create the tunnel:

   ```sh
   cloudflared tunnel login
   cloudflared tunnel create orbit
   ```

2. Forward it in `config.yml`:

   ```yaml
   ingress:
     - hostname: a.example.com
       service: http://127.0.0.1:8787
   ```

    - nested item

      ```json
      {"a": "<b>"}
      ```

Top level:

```sh
echo top
```

```md
1. keep
   ```sh
   not lifted
   ```
```
"""


def test_indented_fences_render_as_code_blocks():
    h = render(DOC)
    assert '<pre><code class="language-sh">cloudflared tunnel login\ncloudflared tunnel create orbit\n</code></pre>' in h
    assert ('<pre><code class="language-yaml">ingress:\n  - hostname: a.example.com\n'
            '    service: http://127.0.0.1:8787\n</code></pre>') in h
    assert '<pre><code class="language-json">{"a": "&lt;b&gt;"}\n</code></pre>' in h
    assert "<code>sh" not in h and "<code>yaml" not in h and "<code>json" not in h
    assert "ORBITFENCE" not in h
    assert h.count("<pre>") == 5
    assert "</ol>\n<pre>" not in h.split("Top level")[0]  # the fences stay inside their list item


def test_top_level_fence_and_fence_inside_fence_untouched():
    h = render(DOC)
    assert "<pre><code class=\"language-sh\">echo top" in h
    assert "1. keep\n   ```sh\n   not lifted" in h


def test_readme_has_no_inline_fence_leak():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    h = render(open(os.path.join(root, "README.md"), encoding="utf-8").read())
    for lang in ("sh", "yaml", "json"):
        assert f"<code>{lang}\n" not in h and f"<code>{lang} " not in h
