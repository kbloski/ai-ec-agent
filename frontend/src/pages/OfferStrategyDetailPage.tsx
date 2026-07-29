import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetOfferStrategyQuery, useUpdateOfferStrategyMutation } from '@/features/offerStrategy/offerStrategyApi'
import {
  useDeleteMessageStrategyMutation,
  useGenerateMessageStrategyMutation,
  useListMessageStrategyForOfferStrategyQuery,
} from '@/features/messageStrategy/messageStrategyApi'

export default function OfferStrategyDetailPage() {
  const id = Number(useParams().id)
  const { data: offerStrategy, isLoading, error } = useGetOfferStrategyQuery(id)

  const list = useListMessageStrategyForOfferStrategyQuery(id)
  const [generate, generateState] = useGenerateMessageStrategyMutation()
  const [deleteMessageStrategy] = useDeleteMessageStrategyMutation()
  const [updateOfferStrategy, updateState] = useUpdateOfferStrategyMutation()

  return (
    <DetailShell
      title={(offerStrategy?.offer_name as string) ?? 'Offer strategy'}
      backTo={offerStrategy ? `/marketing-strategy/${offerStrategy.marketing_strategy_id}` : undefined}
      backLabel="← Marketing strategy"
      data={offerStrategy}
      isLoading={isLoading}
      error={error}
      editable={{
        onSave: (fields) => updateOfferStrategy({ id, fields }).unwrap(),
        isSaving: updateState.isLoading,
      }}
    >
      <ResourceList
        title="Message strategy"
        items={list.data}
        isLoading={list.isLoading}
        error={list.error}
        linkTo={(item) => `/message-strategy/${item.id}`}
        itemLabel={(item) => (item.core_message as string) ?? `#${item.id}`}
        onGenerate={() => offerStrategy && generate(offerStrategy)}
        isGenerating={generateState.isLoading}
        generateLabel="Generuj message strategy"
        onDelete={(item) => deleteMessageStrategy({ id: item.id as number, offerStrategyId: id })}
      />
    </DetailShell>
  )
}
