"""README markdown to HTML for the docs page. Python-Markdown's fenced_code only sees a fence that starts in column 0, so a fence indented
inside a list item (any depth, any language) falls through to inline code and its language tag leaks into the text. Those fences are lifted
out here, rendered as <pre><code>, and put back where their placeholder paragraph ended up."""
import html
import re

import markdown

_OPEN = re.compile(r"^([ \t]*)(`{3,}|~{3,})[ \t]*([\w+.#-]*)[ \t]*$")
_TOKEN = "ORBITFENCE{}X"


def _lift_indented_fences(text):
    lines, out, blocks, i = text.split("\n"), [], [], 0
    while i < len(lines):
        m = _OPEN.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        indent, fence, lang = m.groups()
        j = i + 1
        while j < len(lines):
            s = lines[j].strip()
            if s and s[0] == fence[0] and set(s) == {fence[0]} and len(s) >= len(fence):
                break
            j += 1
        if j >= len(lines):  # unclosed: leave it to the library
            out.extend(lines[i:]); break
        if not indent:  # column 0: fenced_code handles it, copied verbatim so an inner example is never touched
            out.extend(lines[i:j + 1])
        else:
            body = [l[len(indent):] if l.startswith(indent) else l.lstrip() for l in lines[i + 1:j]]
            pad = " " * (-(-len(indent.expandtabs(4)) // 4) * 4)  # Python-Markdown only keeps a block in a list item at a 4-space multiple
            out += ["", pad + _TOKEN.format(len(blocks)), ""]
            blocks.append((lang, "\n".join(body)))
        i = j + 1
    return "\n".join(out), blocks


def render(md_text, extensions=("fenced_code", "tables", "toc")):
    text, blocks = _lift_indented_fences(md_text)
    body = markdown.markdown(text, extensions=list(extensions))
    for n, (lang, code) in enumerate(blocks):
        cls = f' class="language-{lang}"' if lang else ""
        body = body.replace(f"<p>{_TOKEN.format(n)}</p>", f"<pre><code{cls}>{html.escape(code, quote=False)}\n</code></pre>")
    return body
