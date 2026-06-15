#!/usr/bin/env python3
"""Render the "AI Gateway Landscape" category map to assets/landscape.png.

A one-glance map of the list's breadth: 9 categories, each with its most
recognizable gateways. It's a shareable asset (HN/掘金/知乎) and a credibility
signal — "this list covers the whole landscape."

Each entry is a ``(label, match)`` pair: ``label`` is what the card shows,
``match`` is a substring that MUST appear in README.md. ``build_landscape`` is a
pure function and the unit test asserts every ``match`` is present — so the
poster can never name a gateway the list doesn't actually carry (no drift).

PIL is imported lazily inside ``render()`` so the data layer stays importable /
unit-testable on the CI runner (no Pillow there).
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUT = ROOT / "assets" / "landscape.png"


def build_landscape() -> list[dict]:
    """The 9 landscape categories, each: {title, kind, items:[(label, match)]}.

    kind drives the card accent colour: hosted / self / cloud / china / cross.
    """
    def E(label, match=None):
        return (label, match or label)

    return [
        {"title": "Hosted aggregators", "zh": "托管聚合", "kind": "hosted", "items": [
            E("OpenRouter"), E("Vercel AI Gateway"), E("Cloudflare AI Gateway"),
            E("Requesty"), E("AIMLAPI"), E("Novita AI")]},
        {"title": "Self-hosted (OSS)", "zh": "自托管开源", "kind": "self", "items": [
            E("LiteLLM"), E("Portkey Gateway"), E("Bifrost"),
            E("Plano (Arch)", "Plano"), E("LLM Gateway", "theopenco/llmgateway"),
            E("Shepherd SMG", "Shepherd Model Gateway")]},
        {"title": "Enterprise & API-gw", "zh": "企业 & API 网关", "kind": "cloud", "items": [
            E("Kong"), E("Apache APISIX"), E("Envoy AI Gateway"),
            E("Tyk"), E("Gravitee"), E("KrakenD")]},
        {"title": "First-party clouds", "zh": "原厂云", "kind": "cloud", "items": [
            E("AWS Bedrock"), E("Azure APIM", "Azure API Management"),
            E("Vertex AI"), E("Databricks"), E("OpenAI", "OpenAI"),
            E("Cloudflare", "Cloudflare AI Gateway")]},
        {"title": "China ecosystem", "zh": "国内生态", "kind": "china", "items": [
            E("new-api"), E("one-api"), E("Higress"),
            E("GPT-Load"), E("VoAPI"), E("done-hub")]},
        {"title": "Smart routing", "zh": "智能路由", "kind": "cross", "items": [
            E("Not Diamond"), E("Martian"), E("RouteLLM"),
            E("Claude Code Router"), E("NVIDIA LLM Router"), E("Orq.ai")]},
        {"title": "Observability", "zh": "可观测", "kind": "cross", "items": [
            E("Helicone"), E("Portkey"), E("MLflow Gateway", "MLflow AI Gateway"),
            E("Braintrust", "Braintrust Proxy"), E("Respan"), E("vLLora", "vLLora")]},
        {"title": "MCP & agent", "zh": "MCP & Agent", "kind": "cross", "items": [
            E("agentgateway"), E("Lunar.dev"), E("IBM ContextForge"),
            E("MetaMCP"), E("Pomerium"), E("Obot")]},
        {"title": "K8s & inference", "zh": "K8s & 推理", "kind": "self", "items": [
            E("KServe"), E("GPUStack"), E("llm-d"), E("AIBrix", "AIBrix"),
            E("vLLM Prod-Stack", "vLLM Production Stack"),
            E("Inference-Ext", "Gateway API Inference Extension")]},
    ]


def all_matches(landscape: list[dict]) -> list[str]:
    return [m for cat in landscape for (_lab, m) in cat["items"]]


# ── Rendering (PIL only) ─────────────────────────────────────────────────────

W, H = 1280, 900
BG = "#0d1117"
WHITE = "#f0f6fc"
GRAY = "#8b949e"
CARD = "#161b22"
COLORS = {
    "hosted": "#58a6ff", "self": "#3fb950", "cloud": "#e3b341",
    "china": "#f85149", "cross": "#bc8cff",
}


def _cjk_font():
    for p in ("/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/STHeiti Medium.ttc"):
        if Path(p).exists():
            return p
    return None


def render(landscape: list[dict], out: Path = OUT, lang: str = "en") -> Path:
    from PIL import Image, ImageDraw, ImageFont

    fdir = "/System/Library/Fonts/Supplemental/"
    cjk = _cjk_font() if lang == "zh" else None
    # Card titles may be CJK; gateway names + ASCII chrome use Arial.
    bold = lambda s: ImageFont.truetype(fdir + "Arial Bold.ttf", s)
    reg = lambda s: ImageFont.truetype(fdir + "Arial.ttf", s)
    tfont = (lambda s: ImageFont.truetype(cjk, s)) if cjk else bold

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill="#58a6ff")

    title = "AI 网关全景图" if lang == "zh" else "The AI Gateway Landscape"
    sub = ("75+ 网关 / 代理 / 路由 —— 按你的需求分类。github.com/cuihuan/awesome-ai-gateway"
           if lang == "zh" else
           "75+ gateways, proxies & routers — organized by what you need. github.com/cuihuan/awesome-ai-gateway")
    d.text((44, 34), title, font=tfont(40), fill=WHITE)
    d.text((44, 88), sub, font=tfont(20) if cjk else reg(20), fill=GRAY)

    cols, rows = 3, 3
    mx, top, gut = 44, 132, 22
    cw = (W - 2 * mx - (cols - 1) * gut) / cols
    ch = (H - top - 44 - (rows - 1) * gut) / rows

    for i, cat in enumerate(landscape):
        r, c = divmod(i, cols)
        x = mx + c * (cw + gut)
        y = top + r * (ch + gut)
        accent = COLORS[cat["kind"]]
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=12, fill=CARD, outline=accent, width=2)
        # header
        d.rounded_rectangle([x, y, x + cw, y + 40], radius=12, fill=accent)
        d.rectangle([x, y + 20, x + cw, y + 40], fill=accent)  # square off bottom of header
        ctitle = cat.get("zh", cat["title"]) if lang == "zh" else cat["title"]
        d.text((x + 16, y + 9), ctitle, font=tfont(21), fill="#0d1117")
        d.text((x + cw - 52, y + 11), f"{len(cat['items'])}+", font=bold(18), fill="#0d1117")
        # items
        iy = y + 54
        for label, _m in cat["items"]:
            d.ellipse([x + 18, iy + 7, x + 24, iy + 13], fill=accent)
            d.text((x + 34, iy), label, font=bold(19), fill=WHITE)
            iy += 30

    foot = ("内附成本 · 路由 · 安全评分卡 · 真实评测 —— 先选网关，再选模型。" if lang == "zh"
            else "Cost · routing · security scorecard · real-world reviews inside — pick the gateway, then the model.")
    d.text((44, H - 34), foot, font=tfont(18) if cjk else bold(18), fill="#58a6ff")

    out.parent.mkdir(exist_ok=True)
    img.save(out, "PNG")
    return out


def main() -> int:
    land = build_landscape()
    targets = [("en", OUT), ("zh", ROOT / "assets" / "landscape.zh-CN.png")]
    for lang, path in targets:
        try:
            render(land, path, lang)
            print(f"wrote {path} ({path.stat().st_size // 1024} KB)")
        except Exception as e:
            print(f"skipped {path.name}: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
