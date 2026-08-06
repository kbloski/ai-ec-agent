import { useParams } from 'react-router-dom'
import { ResourceList } from '@/components/ResourceList'
import {
  useDeleteKnowledgeMutation,
  useGenerateKnowledgeMutation,
  useListKnowledgeForOfferQuery,
} from '@/features/knowledge/knowledgeApi'

export default function OfferKnowledgesPage() {
  const offerId = Number(useParams().offerId)
  const knowledgeList = useListKnowledgeForOfferQuery(offerId)
  const [generateKnowledge, { isLoading: isGenerating }] = useGenerateKnowledgeMutation()
  const [deleteKnowledge] = useDeleteKnowledgeMutation()

  return (
    <div className="max-w-3xl space-y-6 p-6">
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
