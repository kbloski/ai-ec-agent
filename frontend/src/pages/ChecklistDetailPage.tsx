import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { Button } from '@/components/ui/button'
import { useGenerateChecklistMutation, useGetChecklistQuery } from '@/features/checklists/checklistsApi'

export default function ChecklistDetailPage() {
  const { knowledgeId: knowledgeIdParam, analysisId: analysisIdParam, checklistId: checklistIdParam } =
    useParams()
  const knowledgeId = Number(knowledgeIdParam)
  const analysisId = Number(analysisIdParam)
  const checklistId = Number(checklistIdParam)

  const { data, isLoading, error } = useGetChecklistQuery(checklistId)
  const [generateChecklist, generateState] = useGenerateChecklistMutation()

  return (
    <DetailShell
      title={(data?.name as string) ?? `Checklista #${checklistId}`}
      backTo={`/knowledges/${knowledgeId}/analysis/${analysisId}`}
      backLabel="← Analiza"
      data={data}
      isLoading={isLoading}
      error={error}
    >
      <Button
        size="sm"
        onClick={() => generateChecklist({ knowledgeId, analysisId, checklistId })}
        disabled={generateState.isLoading}
      >
        {generateState.isLoading ? 'Generowanie…' : 'Generuj zadania'}
      </Button>
    </DetailShell>
  )
}
