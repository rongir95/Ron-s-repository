// Builds a single self-contained HTML file from the Vite production build by
// inlining the JS and CSS. The result (feature-brief-builder.standalone.html)
// can be opened directly in a browser — no server or internet required.
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
<meta name="description" content="Create better product context before UX starts designing." />
<title>Feature Brief Builder</title>
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

const out = 'feature-brief-builder.standalone.html'
writeFileSync(out, html)
console.log(`Wrote ${out} (${(html.length / 1024).toFixed(0)} KB)`)
