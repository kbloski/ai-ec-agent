import { Plus } from 'lucide-react'
import { useParams } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { EntityList } from '@/components/EntityList'
import {
  useDeleteKnowledgeMutation,
  useGenerateKnowledgeMutation,
  useListKnowledgeForOfferQuery,
} from '@/features/knowledge/knowledgeApi'

export default function KnowledgesPage() {
  const offerId = Number(useParams().offerId)
  const knowledgeList = useListKnowledgeForOfferQuery(offerId)
  const [generateKnowledge, { isLoading: isGenerating }] = useGenerateKnowledgeMutation()
  const [deleteKnowledge] = useDeleteKnowledgeMutation()

  return (
    <div className="w-full p-6 lg:p-10">
      <EntityList
        title="Knowledges"
        eyebrow="Baza wiedzy"
        items={knowledgeList.data}
        isLoading={knowledgeList.isLoading}
        error={knowledgeList.error}
        linkTo={(item) => `/knowledges/${item.id}`}
        itemLabel={(item) => (item.offer_summary as string) ?? `Knowledge #${item.id}`}
        emptyTitle="Brak bazy wiedzy"
        emptyDescription="Wygeneruj pierwszy element, aby rozpocząć pracę."
        onDelete={(item) => deleteKnowledge({ id: item.id as number, offerId })}
        actions={
          <Button
            onClick={() => generateKnowledge({ offerId })}
            disabled={isGenerating}
            className="h-10 rounded-none px-4"
          >
            <Plus className="size-4" />
            {isGenerating ? 'Generowanie…' : 'Generuj knowledge'}
          </Button>
        }
      />
    </div>
  )
}
