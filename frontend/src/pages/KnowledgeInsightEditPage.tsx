import { useState, type FormEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ChevronDown } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { EntityViewer } from '@/components/EntityViewer'
import { useGetKnowledgeInsightQuery, useUpdateKnowledgeInsightMutation } from '@/features/knowledge/knowledgeApi'
import { useListContentStatusesQuery } from '@/features/contentStatus/contentStatusApi'

export default function KnowledgeInsightEditPage() {
  const id = Number(useParams().id)
  const navigate = useNavigate()

  const { data, isLoading, error } = useGetKnowledgeInsightQuery(id)
  const { data: statuses } = useListContentStatusesQuery()
  const [updateKnowledgeInsight, updateState] = useUpdateKnowledgeInsightMutation()

  const [contentStatus, setContentStatus] = useState<string | undefined>(undefined)

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!data || !contentStatus) return

    await updateKnowledgeInsight({
      id,
      knowledgeId: data.knowledge_id as number,
      content_status: contentStatus,
    }).unwrap()

    navigate(`/knowledges/${data.knowledge_id}`)
  }

  return (
    <div className="mx-auto max-w-xl space-y-6 p-6">
      <h1 className="text-2xl font-semibold">Edytuj insight wiedzy</h1>

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

      {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
      {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>}

      {data && (
        <form onSubmit={handleSubmit} className="space-y-4 rounded-lg border p-4">
          <div className="space-y-1">
            <Label>Typ</Label>
            <p className="text-sm text-muted-foreground">{data.type as string}</p>
          </div>

          <div className="space-y-1">
            <Label>Wartość</Label>
            <p className="text-sm whitespace-pre-wrap">{data.value as string}</p>
          </div>

          <div className="space-y-1">
            <Label htmlFor="content_status">Status</Label>
            <Select
              value={contentStatus ?? (data.content_status as string)}
              onValueChange={setContentStatus}
            >
              <SelectTrigger id="content_status">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {statuses?.map((status) => (
                  <SelectItem key={status.value} value={status.value}>
                    {status.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="flex gap-2">
            <Button type="submit" disabled={updateState.isLoading}>
              {updateState.isLoading ? 'Zapisywanie…' : 'Zapisz'}
            </Button>
            <Button type="button" variant="black" onClick={() => navigate(`/knowledges/${data.knowledge_id}`)}>
              Anuluj
            </Button>
          </div>
        </form>
      )}
    </div>
  )
}
