// Builds a single self-contained HTML file from the Vite production build by
// inlining the JS and CSS. The result can be opened straight from disk — no
// server, no install.
//
// A file:// page cannot proxy /yf, so Yahoo Finance is unreachable from the
// standalone build; it is therefore built with VITE_DEFAULT_PROVIDER=demo and
// opens on offline demo prices. Settings → Twelve Data (free API key) gives it
// real prices, since that provider is callable directly from the browser.
//
// Usage: npm run build:standalone
import { readFileSync, writeFileSync, readdirSync } from 'node:fs'

const assets = 'dist/assets'
const files = readdirSync(assets)
const jsFile = files.find((f) => f.endsWith('.js'))
const cssFile = files.find((f) => f.endsWith('.css'))

if (!jsFile || !cssFile) {
  console.error('Could not find built assets in dist/assets — run `npm run build` first.')
  process.exit(1)
}

const js = readFileSync(`${assets}/${jsFile}`, 'utf8')
const css = readFileSync(`${assets}/${cssFile}`, 'utf8')

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="color-scheme" content="light dark" />
<meta name="description" content="Track individual stock portfolios with near-real-time market data." />
<title>Portfolio</title>
<style>
${css}
</style>
</head>
<body>
<div id="root"></div>
<script type="module">
${js}
</script>
</body>
</html>
`

const out = 'portfolio-dashboard.standalone.html'
writeFileSync(out, html)
console.log(`Wrote ${out} (${(html.length / 1024).toFixed(0)} KB)`)
