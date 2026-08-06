import { Link, useParams } from 'react-router-dom'
import { ResourceList } from '@/components/ResourceList'
import { useGetOfferQuery } from '@/features/offers/offersApi'
import {
  useDeleteKnowledgeMutation,
  useGenerateKnowledgeMutation,
  useListKnowledgeForOfferQuery,
} from '@/features/knowledge/knowledgeApi'

export default function OfferKnowledgesPage() {
  const offerId = Number(useParams().offerId)
  const { data: offer } = useGetOfferQuery(offerId)
  const knowledgeList = useListKnowledgeForOfferQuery(offerId)
  const [generateKnowledge, { isLoading: isGenerating }] = useGenerateKnowledgeMutation()
  const [deleteKnowledge] = useDeleteKnowledgeMutation()

  return (
    <div className="max-w-3xl space-y-6 p-6">
      <Link to={`/offers/${offerId}`} className="text-sm text-muted-foreground hover:underline">
        ← {(offer?.name as string) ?? 'Oferta'}
      </Link>

      <h1 className="text-2xl font-semibold">Knowledge</h1>

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
        onDelete={(item) => deleteKnowledge({ id: item.id as number, offerId })}
      />
    </div>
  )
}
