import { useNavigate, useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { Button } from '@/components/ui/button'
import {
  useDeleteOfferInsightMutation,
  useDeleteOfferItemMutation,
  useDeleteOfferMutation,
  useGenerateOfferSuggestionsMutation,
  useGetOfferQuery,
  useUpdateOfferMutation,
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
  const [deleteOfferInsight] = useDeleteOfferInsightMutation()
  const [deleteOfferItem] = useDeleteOfferItemMutation()
  const [generateSuggestions, generateSuggestionsState] = useGenerateOfferSuggestionsMutation()
  const [updateOffer, updateOfferState] = useUpdateOfferMutation()

  return (
    <DetailShell
      title={offer?.name as string}
      backTo="/"
      backLabel="← Oferty"
      data={offer}
      isLoading={isLoading}
      error={error}
      collapsibleFields={['offer_items', 'offer_insights']}
      itemActions={{
        offer_insights: (item) => deleteOfferInsight({ id: item.id as number, offerId }),
        offer_items: (item) => deleteOfferItem({ id: item.id as number, offerId }),
      }}
      itemLinks={{
        offer_insights: (item) => `/offer-insights/${item.id}/edit`,
        offer_items: (item) => `/offer-items/${item.id}/edit`,
      }}
      editable={{
        onSave: (fields) => updateOffer({ id: offerId, fields }).unwrap(),
        isSaving: updateOfferState.isLoading,
      }}
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
