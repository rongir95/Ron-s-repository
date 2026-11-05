#!/usr/bin/env python3
"""Build fanzone/preview.html: a single self-contained file (CSS, JS, fonts,
images and a short, compressed video clip inlined) for quick in-app preview."""
import base64, mimetypes, pathlib, re, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLIP_SECONDS = 12

def data_uri(path: pathlib.Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or ('font/woff2' if path.suffix == '.woff2' else 'application/octet-stream')
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"

def inline_assets(text: str, clip: pathlib.Path) -> str:
    def repl(m):
        rel = m.group(0)
        if rel.endswith('.mp4'):
            return data_uri(clip)
        p = ROOT / rel
        return data_uri(p) if p.exists() else rel
    return re.sub(r"assets/[\w./-]+\.(?:png|jpg|svg|woff2|mp4)", repl, text)

with tempfile.TemporaryDirectory() as tmp:
    clip = pathlib.Path(tmp) / 'clip.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(ROOT / 'assets/video/match-bg.mp4'),
                    '-t', str(CLIP_SECONDS), '-an', '-vf', 'scale=640:-2', '-c:v', 'libx264',
                    '-crf', '34', '-preset', 'slow', '-movflags', '+faststart', str(clip)], check=True)
    html = (ROOT / 'index.html').read_text()
    # Some in-app previews block data: video sources, so load the clip via a blob URL;
    # the inlined poster frame still shows if video is blocked entirely.
    html = html.replace('src="assets/video/match-bg.mp4" ', '')
    clip_b64 = base64.b64encode(clip.read_bytes()).decode()
    blob_loader = ("<script>(() => { const v = document.querySelector('video');"
                   f" const b = Uint8Array.from(atob('{clip_b64}'), (c) => c.charCodeAt(0));"
                   " v.src = URL.createObjectURL(new Blob([b], { type: 'video/mp4' })); })();</script>\n  ")
    css = inline_assets((ROOT / 'styles.css').read_text(), clip)
    js = inline_assets((ROOT / 'app.js').read_text(), clip)
    html = html.replace('<link rel="stylesheet" href="styles.css">', f'<style>\n{css}\n</style>')
    html = html.replace('<script src="app.js"></script>', blob_loader + f'<script>\n{js}\n</script>')
    html = inline_assets(html, clip)
    out = ROOT / 'preview.html'
    out.write_text(html)
    print(f"{out} ({out.stat().st_size / 1e6:.1f} MB)")
