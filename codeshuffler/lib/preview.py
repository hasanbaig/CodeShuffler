from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Any, Dict, List, Optional, Tuple


class PreviewError(RuntimeError):
    pass


@dataclass(frozen=True)
class HtmlPreview:
    html: str


def render_exam_html(
    exam_dict: Dict[Any, Any],
    *,
    title: str = "Exam Preview",
    subtitle: Optional[str] = None,
) -> HtmlPreview:
    """
    Convert the parsed/shuffled exam structure into an HTML preview.

    This is intentionally tolerant of different exam_dict shapes since parse_exam()
    may evolve. We attempt to render something sensible for:
      - {qnum: list[str]} (choices only)
      - {qnum: {"prompt": str, "choices": list[str], ...}}
      - {qnum: tuple/list containing prompt + choices}
      - Any other value -> stringified

    The goal of preview is clarity for instructors (order, choices, code blocks),
    not perfect Word fidelity.
    """
    if not exam_dict:
        raise PreviewError("No exam content to preview.")

    # Sort questions if possible
    items = list(exam_dict.items())
    try:
        items.sort(key=lambda kv: int(kv[0]))
    except Exception:
        # Fall back to insertion order
        pass

    css = _default_css()

    header_bits = [f"<h1>{escape(title)}</h1>"]
    if subtitle:
        header_bits.append(f"<p class='subtitle'>{escape(subtitle)}</p>")

    body = []
    body.append("<div class='page'>")
    body.append("<div class='header'>")
    body.extend(header_bits)
    body.append("</div>")

    body.append("<div class='questions'>")

    for idx, (qnum, qval) in enumerate(items, start=1):
        prompt, choices, meta = _coerce_question(qnum, qval, idx=idx)

        body.append("<section class='question'>")
        body.append(
            f"<div class='qtitle'><span class='qnum'>Q{escape(str(qnum))}</span>"
            f"<span class='qidx'>({idx})</span></div>"
        )

        if prompt:
            body.append(f"<div class='prompt'>{_render_rich_text(prompt)}</div>")

        if choices:
            body.append("<ol class='choices'>")
            for c in choices:
                body.append(f"<li class='choice'>{_render_rich_text(c)}</li>")
            body.append("</ol>")

        # Optional meta display if ever useful (kept off by default)
        # if meta:
        #     body.append(f"<pre class='meta'>{escape(str(meta))}</pre>")

        body.append("</section>")

    body.append("</div>")  # questions
    body.append("</div>")  # page

    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{escape(title)}</title>
  <style>{css}</style>
</head>
<body>
  {''.join(body)}
</body>
</html>
"""
    return HtmlPreview(html=html)


def _coerce_question(qnum: Any, qval: Any, *, idx: int) -> Tuple[str, List[str], Dict[str, Any]]:
    """
    Normalize many potential question shapes into:
      prompt: str
      choices: list[str]
      meta: dict[str, Any]
    """
    meta: Dict[str, Any] = {}

    # Shape A: {qnum: {"prompt":..., "choices":[...], ...}}
    if isinstance(qval, dict):
        prompt = ""
        for k in ("prompt", "question", "stem", "text"):
            if k in qval and isinstance(qval[k], str):
                prompt = qval[k]
                break

        choices_val = None
        for k in ("choices", "options", "answers", "mcq"):
            if k in qval and isinstance(qval[k], (list, tuple)):
                choices_val = qval[k]
                break

        choices = [str(x) for x in choices_val] if choices_val else []

        # Keep the rest as meta (optional)
        for k, v in qval.items():
            if k not in (
                "prompt",
                "question",
                "stem",
                "text",
                "choices",
                "options",
                "answers",
                "mcq",
            ):
                meta[k] = v

        if not prompt and not choices:
            prompt = str(qval)

        return prompt, choices, meta

    # Shape B: {qnum: list[str]} (choices only)
    if isinstance(qval, (list, tuple)):
        # If it looks like (prompt, choices)
        if len(qval) == 2 and isinstance(qval[0], str) and isinstance(qval[1], (list, tuple)):
            prompt = qval[0]
            choices = [str(x) for x in qval[1]]
            return prompt, choices, meta

        # Otherwise assume it's a list of choices
        choices = [str(x) for x in qval]
        prompt = f"Question {idx}"
        return prompt, choices, meta

    # Shape C: single string
    if isinstance(qval, str):
        return qval, [], meta

    # Fallback
    return str(qval), [], meta


def _render_rich_text(text: str) -> str:
    """
    Very lightweight "rich" rendering:
    - Escapes HTML
    - Detects fenced code blocks ```...``` and renders as <pre><code>...</code></pre>
    - Preserves line breaks
    """
    s = text.strip()
    if "```" not in s:
        return _render_paragraphs(s)

    parts = s.split("```")
    out: List[str] = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # normal text
            if part.strip():
                out.append(_render_paragraphs(part))
        else:
            # code block (optionally with language as first line)
            code = part
            code_lines = code.splitlines()
            if code_lines and len(code_lines[0].strip()) <= 20 and " " not in code_lines[0].strip():
                # could be "python" or "cpp" etc
                # we ignore language but strip it from displayed code
                code_lines = code_lines[1:]
            code_clean = "\n".join(code_lines).rstrip("\n")
            out.append(f"<pre class='code'><code>{escape(code_clean)}</code></pre>")
    return "".join(out)


def _render_paragraphs(text: str) -> str:
    # Preserve blank lines as paragraph breaks
    lines = text.splitlines()
    paras: List[List[str]] = [[]]
    for line in lines:
        if line.strip() == "":
            if paras[-1]:
                paras.append([])
            continue
        paras[-1].append(line)

    html_paras: List[str] = []
    for p in paras:
        if not p:
            continue
        joined = "\n".join(p)
        html_paras.append("<p>{}</p>".format(escape(joined).replace("\n", "<br/>")))
    return "".join(html_paras)


def _default_css() -> str:
    # Dark, clean, exam-like. Works well in both WebEngine and QTextBrowser.
    return r"""
:root {
  --bg: #ffffff;
  --panel: #f6f6f6;
  --text: #1e1e1e;
  --muted: #666666;
  --border: #d0d0d0;
  --accent: #2b6cb0;
  --codebg: #f0f0f0;
}

html, body {
  background: var(--bg);
  color: var(--text);
}


.page {
  max-width: 880px;
  margin: 0 auto;
  padding: 18px 16px 28px 16px;
}

.header {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px 14px 10px 14px;
  margin-bottom: 14px;
}

h1 {
  font-size: 18px;
  margin: 0 0 6px 0;
}

.subtitle {
  margin: 0;
  color: var(--muted);
}

.questions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.question {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px 12px;
}

.qtitle {
  display: flex;
  gap: 8px;
  align-items: baseline;
  margin-bottom: 8px;
}

.qnum {
  color: var(--accent);
  font-weight: 700;
}

.qidx {
  color: var(--muted);
}

.prompt p {
  margin: 0 0 8px 0;
}

.choices {
  margin: 0;
  padding-left: 20px;
}

.choice {
  margin: 6px 0;
  color: var(--text);
}

.code {
  background: var(--codebg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px;
  overflow-x: auto;
}

.code code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
  font-size: 12.5px;
  line-height: 1.35;
  color: var(--text);
}
"""
