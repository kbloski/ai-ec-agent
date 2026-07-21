import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { Button } from '@/components/ui/button'
import {
  useDeleteChecklistItemMutation,
  useGenerateChecklistMutation,
  useGetChecklistQuery,
} from '@/features/checklists/checklistsApi'
import type { Entity } from '@/types'

export default function ChecklistDetailPage() {
  const { knowledgeId: knowledgeIdParam, analysisId: analysisIdParam, checklistId: checklistIdParam } =
    useParams()
  const knowledgeId = Number(knowledgeIdParam)
  const analysisId = Number(analysisIdParam)
  const checklistId = Number(checklistIdParam)

  const { data, isLoading, error } = useGetChecklistQuery(checklistId)
  const [generateChecklist, generateState] = useGenerateChecklistMutation()
  const [deleteChecklistItem] = useDeleteChecklistItemMutation()

  return (
    <DetailShell
      title={(data?.name as string) ?? `Checklista #${checklistId}`}
      backTo={`/knowledges/${knowledgeId}/analysis/${analysisId}`}
      backLabel="← Analiza"
      data={data}
      isLoading={isLoading}
      error={error}
      exclude={['checklist_items']}
    >
      <Button
        size="sm"
        onClick={() => generateChecklist({ knowledgeId, analysisId, checklistId })}
        disabled={generateState.isLoading}
      >
        {generateState.isLoading ? 'Generowanie…' : 'Generuj zadania'}
      </Button>

      <ResourceList
        title="Zadania"
        items={data?.checklist_items as Entity[] | undefined}
        isLoading={isLoading}
        error={error}
        itemLabel={(item) => (item.title as string) ?? `#${item.id}`}
        onDelete={(item) => deleteChecklistItem({ id: item.id as number, checklistId })}
      />
    </DetailShell>
  )
}
