import { useState } from 'react'
import { Check, Copy } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface EntityViewerProps {
  data: unknown
  className?: string
}

/** Uniwersalny podgląd dowolnej encji w postaci sformatowanego JSON-a. */
export function EntityViewer({ data, className }: EntityViewerProps) {
  const [copied, setCopied] = useState(false)

  const json = JSON.stringify(data, null, 2)

  async function handleCopy() {
    await navigator.clipboard.writeText(json)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className={cn('rounded-lg border bg-card text-card-foreground shadow-sm p-4', className)}>
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-sm font-medium text-muted-foreground">JSON</h3>
        <Button variant="outline" size="sm" onClick={handleCopy}>
          {copied ? (
            <>
              <Check /> Copied!
            </>
          ) : (
            <>
              <Copy /> Copy JSON
            </>
          )}
        </Button>
      </div>
      <pre className="max-h-[32rem] overflow-auto rounded-md bg-muted p-3 text-xs whitespace-pre-wrap break-words">{json}</pre>
    </div>
  )
}
