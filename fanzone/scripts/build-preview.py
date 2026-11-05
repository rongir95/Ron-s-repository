#!/usr/bin/env python3
"""Build fanzone/preview.html: a single self-contained file (CSS, JS, fonts,
images and an animated WebP loop of the match inlined) for quick in-app preview."""
import base64, mimetypes, pathlib, re, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLIP_SECONDS = 6
LOOP_FPS = 10
LOOP_WIDTH = 720

def data_uri(path: pathlib.Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or ('font/woff2' if path.suffix == '.woff2' else 'application/octet-stream')
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"

def inline_assets(text: str) -> str:
    def repl(m):
        rel = m.group(0)
        p = ROOT / rel
        return data_uri(p) if p.exists() else rel
    return re.sub(r"assets/[\w./-]+\.(?:png|jpg|svg|woff2|mp4)", repl, text)

with tempfile.TemporaryDirectory() as tmp:
    html = (ROOT / 'index.html').read_text()
    # The in-app file viewer doesn't play <video>, so the preview swaps it for an
    # animated WebP loop of the match (images always animate there).
    loop = pathlib.Path(tmp) / 'loop.webp'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '2', '-t', str(CLIP_SECONDS),
                    '-i', str(ROOT / 'assets/video/match-bg.mp4'), '-an',
                    '-vf', f'fps={LOOP_FPS},scale={LOOP_WIDTH}:-2:flags=lanczos', '-c:v', 'libwebp_anim',
                    '-loop', '0', '-q:v', '80', '-compression_level', '6', str(loop)], check=True)
    html = re.sub(r'<video [^>]*></video>',
                  f'<img class="video-loop" src="{data_uri(loop)}" alt="Live match">', html)
    css = inline_assets((ROOT / 'styles.css').read_text())
    js = inline_assets((ROOT / 'app.js').read_text())
    html = html.replace('<link rel="stylesheet" href="styles.css">', f'<style>\n{css}\n</style>')
    html = html.replace('<script src="app.js"></script>', f'<script>\n{js}\n</script>')
    html = inline_assets(html)
    out = ROOT / 'preview.html'
    out.write_text(html)
    print(f"{out} ({out.stat().st_size / 1e6:.1f} MB)")
