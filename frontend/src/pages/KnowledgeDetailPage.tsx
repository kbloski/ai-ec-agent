import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import {
  useDeleteKnowledgeInsightMutation,
  useGetKnowledgeQuery,
  useUpdateKnowledgeInsightMutation,
  useUpdateKnowledgeMutation,
} from '@/features/knowledge/knowledgeApi'
import {
  useDeleteTargetAudienceMutation,
  useUpdateTargetAudienceMutation,
} from '@/features/targetAudiences/targetAudiencesApi'
import {
  useCreateAnalysisMutation,
  useDeleteAnalysisMutation,
  useListAnalysisForKnowledgeQuery,
} from '@/features/analysis/analysisApi'
import {
  useDeleteBrandMarketingMutation,
  useGenerateBrandMarketingMutation,
  useListBrandMarketingForKnowledgeQuery,
} from '@/features/brandMarketing/brandMarketingApi'

export default function KnowledgeDetailPage() {
  const knowledgeId = Number(useParams().knowledgeId)
  const { data: knowledge, isLoading, error } = useGetKnowledgeQuery(knowledgeId)

  const [deleteKnowledgeInsight] = useDeleteKnowledgeInsightMutation()
  const [updateKnowledgeInsight] = useUpdateKnowledgeInsightMutation()
  const [deleteTargetAudience] = useDeleteTargetAudienceMutation()
  const [updateTargetAudience] = useUpdateTargetAudienceMutation()

  const analysisList = useListAnalysisForKnowledgeQuery(knowledgeId)
  const [createAnalysis, createAnalysisState] = useCreateAnalysisMutation()
  const [deleteAnalysis] = useDeleteAnalysisMutation()

  const brandMarketingList = useListBrandMarketingForKnowledgeQuery(knowledgeId)
  const [generateBrandMarketing, generateBrandMarketingState] = useGenerateBrandMarketingMutation()
  const [deleteBrandMarketing] = useDeleteBrandMarketingMutation()

  const [updateKnowledge, updateKnowledgeState] = useUpdateKnowledgeMutation()

  return (
    <DetailShell
      title="Knowledge"
      backTo={knowledge ? `/offers/${knowledge.offer_id}` : undefined}
      backLabel="← Oferta"
      data={knowledge}
      isLoading={isLoading}
      error={error}
      itemActions={{
        offer_insights: (item) => deleteKnowledgeInsight({ id: item.id as number, knowledgeId }),
        target_audiences: (item) => deleteTargetAudience({ id: item.id as number, knowledgeId }),
      }}
      itemLinks={{
        offer_insights: (item) => `/knowledge-insights/${item.id}/edit`,
        target_audiences: (item) => `/target-audiences/${item.id}/edit`,
      }}
      relationLinks={{
        offer_insights: `/knowledges/${knowledgeId}/insights`,
        target_audiences: `/knowledges/${knowledgeId}/target-audiences`,
      }}
      itemStatusActions={{
        offer_insights: (item, contentStatus) =>
          updateKnowledgeInsight({
            id: item.id as number,
            knowledgeId,
            content_status: contentStatus,
          }).unwrap(),
        target_audiences: (item, contentStatus) =>
          updateTargetAudience({
            id: item.id as number,
            knowledgeId,
            content_status: contentStatus,
          }).unwrap(),
      }}
      editable={{
        onSave: (fields) => updateKnowledge({ id: knowledgeId, fields }).unwrap(),
        isSaving: updateKnowledgeState.isLoading,
      }}
    >
      <ResourceList
        title="Analizy"
        items={analysisList.data}
        isLoading={analysisList.isLoading}
        error={analysisList.error}
        linkTo={(item) => `/knowledges/${knowledgeId}/analysis/${item.id}`}
        itemLabel={(item) => `Analiza #${item.id}`}
        onGenerate={() => createAnalysis({ knowledgeId })}
        isGenerating={createAnalysisState.isLoading}
        generateLabel="Utwórz analizę"
        onDelete={(item) => deleteAnalysis({ id: item.id as number, knowledgeId })}
      />

      <ResourceList
        title="Brand marketing"
        items={brandMarketingList.data}
        isLoading={brandMarketingList.isLoading}
        error={brandMarketingList.error}
        linkTo={(item) => `/brand-marketing/${item.id}`}
        itemLabel={(item) => (item.brand_name as string) ?? `#${item.id}`}
        onGenerate={() => generateBrandMarketing({ knowledgeId })}
        isGenerating={generateBrandMarketingState.isLoading}
        generateLabel="Generuj brand marketing"
        onDelete={(item) => deleteBrandMarketing({ id: item.id as number, knowledgeId })}
      />

    </DetailShell>
  )
}
