import { useEffect, useState } from 'react'
import { ChevronDown } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { EntityViewer } from '@/components/EntityViewer'
import { useGetOutputPromptQuery, useSaveOutputPromptMutation } from '@/features/settings/settingsApi'

export default function SettingsPage() {
  const { data, isLoading, error } = useGetOutputPromptQuery()
  const [saveOutputPrompt, saveState] = useSaveOutputPromptMutation()

  const [content, setContent] = useState('')

  useEffect(() => {
    if (data) setContent(data.content)
  }, [data])

  return (
    <div className="max-w-3xl space-y-6 p-6">
      <h1 className="text-2xl font-semibold">Ustawienia</h1>

      {data && (
        <Collapsible>
          <CollapsibleTrigger className="group flex items-center gap-1.5 text-xs font-medium tracking-wide text-muted-foreground uppercase hover:text-foreground">
            <ChevronDown className="size-3.5 shrink-0 transition-transform group-data-[panel-open]:rotate-180" />
            Pokaż surowy JSON
          </CollapsibleTrigger>
          <CollapsibleContent className="pt-2">
            <EntityViewer data={data} />
          </CollapsibleContent>
        </Collapsible>
      )}

      <div className="space-y-2">
        <h2 className="text-sm font-medium">Output prompt</h2>
        <p className="text-sm text-muted-foreground">
          Treść instrukcji formatowania odpowiedzi dołączana do każdego zapytania do modelu LLM.
        </p>

        {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
        {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>}

        {!isLoading && (
          <>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={20}
              className="w-full rounded-lg border border-border bg-background p-3 font-mono text-sm outline-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50"
            />

            <div className="flex items-center gap-3">
              <Button onClick={() => saveOutputPrompt(content)} disabled={saveState.isLoading}>
                {saveState.isLoading ? 'Zapisywanie…' : 'Zapisz'}
              </Button>
              {saveState.isSuccess && <span className="text-sm text-muted-foreground">Zapisano.</span>}
              {saveState.isError && <span className="text-sm text-destructive">Nie udało się zapisać.</span>}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
