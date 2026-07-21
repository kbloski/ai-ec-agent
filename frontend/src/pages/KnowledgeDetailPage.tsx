import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { Button } from '@/components/ui/button'
import { useGetKnowledgeQuery } from '@/features/knowledge/knowledgeApi'
import { useGenerateTargetAudiencesMutation } from '@/features/targetAudiences/targetAudiencesApi'
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

  const [generateAudiences, generateAudiencesState] = useGenerateTargetAudiencesMutation()

  const analysisList = useListAnalysisForKnowledgeQuery(knowledgeId)
  const [createAnalysis, createAnalysisState] = useCreateAnalysisMutation()
  const [deleteAnalysis] = useDeleteAnalysisMutation()

  const brandMarketingList = useListBrandMarketingForKnowledgeQuery(knowledgeId)
  const [generateBrandMarketing, generateBrandMarketingState] = useGenerateBrandMarketingMutation()
  const [deleteBrandMarketing] = useDeleteBrandMarketingMutation()

  return (
    <DetailShell
      title="Knowledge"
      backTo={knowledge ? `/offers/${knowledge.offer_id}` : undefined}
      backLabel="← Oferta"
      data={knowledge}
      isLoading={isLoading}
      error={error}
      collapsibleFields={['offer_insights', 'target_audiences']}
    >
      <Button
        size="sm"
        onClick={() => generateAudiences({ knowledgeId })}
        disabled={generateAudiencesState.isLoading}
      >
        {generateAudiencesState.isLoading ? 'Generowanie…' : 'Generuj grupy docelowe'}
      </Button>

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
