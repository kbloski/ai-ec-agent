import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetOfferQuery } from '@/features/offers/offersApi'
import {
  useGenerateKnowledgeMutation,
  useListKnowledgeForOfferQuery,
} from '@/features/knowledge/knowledgeApi'

export default function OfferDetailPage() {
  const offerId = Number(useParams().offerId)
  const { data: offer, isLoading, error } = useGetOfferQuery(offerId)

  const knowledgeList = useListKnowledgeForOfferQuery(offerId)
  const [generateKnowledge, { isLoading: isGenerating }] = useGenerateKnowledgeMutation()

  return (
    <DetailShell title={offer?.name as string} backTo="/" backLabel="← Oferty" data={offer} isLoading={isLoading} error={error}>
      <ResourceList
        title="Knowledge"
        items={knowledgeList.data}
        isLoading={knowledgeList.isLoading}
        error={knowledgeList.error}
        linkTo={(item) => `/knowledges/${item.id}`}
        itemLabel={(item) => (item.offer_summary as string) ?? `#${item.id}`}
        onGenerate={() => generateKnowledge({ offerId })}
        isGenerating={isGenerating}
        generateLabel="Generuj knowledge"
      />
    </DetailShell>
  )
}
