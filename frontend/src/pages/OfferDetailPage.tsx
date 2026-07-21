import { useNavigate, useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { Button } from '@/components/ui/button'
import {
  useDeleteOfferMutation,
  useGenerateOfferSuggestionsMutation,
  useGetOfferQuery,
} from '@/features/offers/offersApi'
import {
  useDeleteKnowledgeMutation,
  useGenerateKnowledgeMutation,
  useListKnowledgeForOfferQuery,
} from '@/features/knowledge/knowledgeApi'

export default function OfferDetailPage() {
  const offerId = Number(useParams().offerId)
  const navigate = useNavigate()
  const { data: offer, isLoading, error } = useGetOfferQuery(offerId)

  const knowledgeList = useListKnowledgeForOfferQuery(offerId)
  const [generateKnowledge, { isLoading: isGenerating }] = useGenerateKnowledgeMutation()
  const [deleteKnowledge] = useDeleteKnowledgeMutation()
  const [deleteOffer] = useDeleteOfferMutation()
  const [generateSuggestions, generateSuggestionsState] = useGenerateOfferSuggestionsMutation()

  return (
    <DetailShell
      title={offer?.name as string}
      backTo="/"
      backLabel="← Oferty"
      data={offer}
      isLoading={isLoading}
      error={error}
      collapsibleFields={['offer_items', 'offer_insights']}
    >
      <Button
        size="sm"
        variant="black"
        onClick={() => {
          if (window.confirm('Czy na pewno usunąć tę ofertę?')) {
            deleteOffer(offerId).then(() => navigate('/'))
          }
        }}
      >
        Usuń ofertę
      </Button>

      <Button
        size="sm"
        onClick={() => generateSuggestions(offerId)}
        disabled={generateSuggestionsState.isLoading}
      >
        {generateSuggestionsState.isLoading ? 'Generowanie…' : 'Generuj sugestie'}
      </Button>

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
    </DetailShell>
  )
}
