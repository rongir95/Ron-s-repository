/** Backup, restore and CSV export. The portfolio lives in this browser, so a
 *  one-click backup file is the safety net — and the way one brother hands a
 *  portfolio to another. */
import type { AppData, Portfolio } from '../types'
import { averageCost, totalShares } from './calc'

function download(filename: string, mime: string, contents: string): void {
  const blob = new Blob([contents], { type: `${mime};charset=utf-8` })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  document.body.appendChild(anchor)
  anchor.click()
  anchor.remove()
  // Give the browser a moment to start the download before revoking.
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

function stamp(): string {
  return new Date().toISOString().slice(0, 10)
}

function slug(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'portfolio'
}

export function exportAll(data: AppData): void {
  download(`portfolios-${stamp()}.json`, 'application/json', JSON.stringify(data, null, 2))
}

export function exportPortfolio(portfolio: Portfolio): void {
  const payload: AppData = {
    version: 1,
    portfolios: [portfolio],
    activePortfolioId: portfolio.id,
    settings: {
      providerId: 'yahoo',
      twelveDataKey: '',
      theme: 'system',
      refreshSeconds: 60,
      privacyMode: false,
    },
  }
  download(`${slug(portfolio.name)}-${stamp()}.json`, 'application/json', JSON.stringify(payload, null, 2))
}

function csvCell(value: string | number): string {
  const text = String(value)
  return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text
}

/** One row per purchase, so a multi-lot holding round-trips into a spreadsheet. */
export function exportCsv(portfolio: Portfolio): void {
  const header = ['Symbol', 'Name', 'Shares', 'Price paid', 'Purchase date', 'Position shares', 'Position avg cost', 'Notes']
  const lines = [header.join(',')]
  for (const position of portfolio.positions) {
    const shares = totalShares(position)
    const avg = averageCost(position)
    for (const lot of position.lots) {
      lines.push(
        [
          position.symbol,
          position.name ?? '',
          lot.shares,
          lot.price,
          lot.date ?? '',
          shares,
          avg.toFixed(4),
          position.notes ?? '',
        ]
          .map(csvCell)
          .join(','),
      )
    }
  }
  download(`${slug(portfolio.name)}-${stamp()}.csv`, 'text/csv', lines.join('\n'))
}

/** Reads a JSON backup chosen by the user. Resolves to the raw parsed value;
 *  the caller normalises it. */
export function pickJsonFile(): Promise<unknown> {
  return new Promise((resolve, reject) => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'application/json,.json'
    input.onchange = async () => {
      const file = input.files?.[0]
      if (!file) {
        reject(new Error('No file chosen.'))
        return
      }
      try {
        resolve(JSON.parse(await file.text()))
      } catch {
        reject(new Error('That file is not valid JSON.'))
      }
    }
    input.click()
  })
}
