import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { Button } from '@/components/ui/button'
import type { Entity } from '@/types'
import {
  useDeleteAnalysisQuestionMutation,
  useGenerateAnalysisAnswersMutation,
  useGetAnalysisQuery,
} from '@/features/analysis/analysisApi'
import {
  useCreateChecklistMutation,
  useDeleteChecklistMutation,
  useListChecklistsForAnalysisQuery,
} from '@/features/checklists/checklistsApi'

export default function AnalysisDetailPage() {
  const { knowledgeId: knowledgeIdParam, analysisId: analysisIdParam } = useParams()
  const knowledgeId = Number(knowledgeIdParam)
  const analysisId = Number(analysisIdParam)

  const { data: analysis, isLoading, error } = useGetAnalysisQuery(analysisId)
  const [generateAnswers, generateAnswersState] = useGenerateAnalysisAnswersMutation()
  const [deleteAnalysisQuestion] = useDeleteAnalysisQuestionMutation()

  const checklists = useListChecklistsForAnalysisQuery(analysisId)
  const [createChecklist, createChecklistState] = useCreateChecklistMutation()
  const [deleteChecklist] = useDeleteChecklistMutation()

  return (
    <DetailShell
      title={`Analiza #${analysisId}`}
      backTo={`/knowledges/${knowledgeId}`}
      backLabel="← Knowledge"
      data={analysis}
      isLoading={isLoading}
      error={error}
      exclude={['anlysis_questions']}
    >
      <div>
        <Button
          size="sm"
          onClick={() => generateAnswers({ knowledgeId, analysisId })}
          disabled={generateAnswersState.isLoading}
        >
          {generateAnswersState.isLoading ? 'Generowanie…' : 'Generuj odpowiedzi'}
        </Button>
      </div>

      <ResourceList
        title="Checklisty"
        items={checklists.data}
        isLoading={checklists.isLoading}
        error={checklists.error}
        linkTo={(item) => `/knowledges/${knowledgeId}/analysis/${analysisId}/checklists/${item.id}`}
        itemLabel={(item) => (item.name as string) ?? `#${item.id}`}
        onGenerate={() => createChecklist({ knowledgeId, analysisId })}
        isGenerating={createChecklistState.isLoading}
        generateLabel="Utwórz checklistę"
        onDelete={(item) => deleteChecklist({ id: item.id as number, analysisId })}
      />

      <ResourceList
        title="Pytania"
        items={analysis?.anlysis_questions as Entity[] | undefined}
        isLoading={isLoading}
        error={error}
        itemLabel={(item) => (item.question as string) ?? `#${item.id}`}
        onDelete={(item) => deleteAnalysisQuestion({ id: item.id as number, analysisId })}
      />
    </DetailShell>
  )
}
