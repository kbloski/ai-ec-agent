import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetKnowledgeQuery } from '@/features/knowledge/knowledgeApi'
import {
  useGenerateTargetAudiencesMutation,
  useListTargetAudiencesForKnowledgeQuery,
} from '@/features/targetAudiences/targetAudiencesApi'
import { useCreateAnalysisMutation, useListAnalysisForKnowledgeQuery } from '@/features/analysis/analysisApi'
import {
  useGenerateBrandMarketingMutation,
  useListBrandMarketingForKnowledgeQuery,
} from '@/features/brandMarketing/brandMarketingApi'

export default function KnowledgeDetailPage() {
  const knowledgeId = Number(useParams().knowledgeId)
  const { data: knowledge, isLoading, error } = useGetKnowledgeQuery(knowledgeId)

  const audiences = useListTargetAudiencesForKnowledgeQuery(knowledgeId)
  const [generateAudiences, generateAudiencesState] = useGenerateTargetAudiencesMutation()

  const analysisList = useListAnalysisForKnowledgeQuery(knowledgeId)
  const [createAnalysis, createAnalysisState] = useCreateAnalysisMutation()

  const brandMarketingList = useListBrandMarketingForKnowledgeQuery(knowledgeId)
  const [generateBrandMarketing, generateBrandMarketingState] = useGenerateBrandMarketingMutation()

  return (
    <DetailShell
      title="Knowledge"
      backTo={knowledge ? `/offers/${knowledge.offer_id}` : undefined}
      backLabel="← Oferta"
      data={knowledge}
      isLoading={isLoading}
      error={error}
    >
      <ResourceList
        title="Grupy docelowe"
        items={audiences.data}
        isLoading={audiences.isLoading}
        error={audiences.error}
        linkTo={(item) => `/target-audiences/${item.id}`}
        onGenerate={() => generateAudiences({ knowledgeId })}
        isGenerating={generateAudiencesState.isLoading}
        generateLabel="Generuj grupy docelowe"
      />

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
      />
    </DetailShell>
  )
}
