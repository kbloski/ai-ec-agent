import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetMessageStrategyQuery } from '@/features/messageStrategy/messageStrategyApi'
import {
  useDeleteAdStrategyMutation,
  useGenerateAdStrategyMutation,
  useListAdStrategyForMessageStrategyQuery,
} from '@/features/adStrategy/adStrategyApi'
import {
  useDeleteUgcCreativeMutation,
  useGenerateUgcCreativesMutation,
  useListUgcCreativesForMessageStrategyQuery,
} from '@/features/ugcCreatives/ugcCreativesApi'
import {
  useDeletePageStrategyMutation,
  useGeneratePageStrategyMutation,
  useListPageStrategyForMessageStrategyQuery,
} from '@/features/pageStrategy/pageStrategyApi'

export default function MessageStrategyDetailPage() {
  const id = Number(useParams().id)
  const { data: messageStrategy, isLoading, error } = useGetMessageStrategyQuery(id)

  const adStrategies = useListAdStrategyForMessageStrategyQuery(id)
  const [generateAdStrategy, generateAdStrategyState] = useGenerateAdStrategyMutation()
  const [deleteAdStrategy] = useDeleteAdStrategyMutation()

  const ugcCreatives = useListUgcCreativesForMessageStrategyQuery(id)
  const [generateUgc, generateUgcState] = useGenerateUgcCreativesMutation()
  const [deleteUgcCreative] = useDeleteUgcCreativeMutation()

  const pageStrategies = useListPageStrategyForMessageStrategyQuery(id)
  const [generatePageStrategy, generatePageStrategyState] = useGeneratePageStrategyMutation()
  const [deletePageStrategy] = useDeletePageStrategyMutation()

  return (
    <DetailShell
      title={(messageStrategy?.core_message as string) ?? 'Message strategy'}
      backTo={messageStrategy ? `/offer-strategy/${messageStrategy.offer_strategy_id}` : undefined}
      backLabel="← Offer strategy"
      data={messageStrategy}
      isLoading={isLoading}
      error={error}
    >
      <ResourceList
        title="Ad strategy"
        items={adStrategies.data}
        isLoading={adStrategies.isLoading}
        error={adStrategies.error}
        linkTo={(item) => `/ad-strategy/${item.id}`}
        itemLabel={(item) => `#${item.id}`}
        onGenerate={() => messageStrategy && generateAdStrategy(messageStrategy)}
        isGenerating={generateAdStrategyState.isLoading}
        generateLabel="Generuj ad strategy"
        onDelete={(item) => deleteAdStrategy({ id: item.id as number, messageStrategyId: id })}
      />

      <ResourceList
        title="UGC creatives"
        items={ugcCreatives.data}
        isLoading={ugcCreatives.isLoading}
        error={ugcCreatives.error}
        linkTo={(item) => `/ugc-creatives/${item.id}`}
        itemLabel={(item) => (item.name as string) ?? `#${item.id}`}
        onGenerate={() => messageStrategy && generateUgc(messageStrategy)}
        isGenerating={generateUgcState.isLoading}
        generateLabel="Generuj UGC creatives"
        onDelete={(item) => deleteUgcCreative({ id: item.id as number, messageStrategyId: id })}
      />

      <ResourceList
        title="Page strategy"
        items={pageStrategies.data}
        isLoading={pageStrategies.isLoading}
        error={pageStrategies.error}
        linkTo={(item) => `/page-strategy/${item.id}`}
        itemLabel={(item) => (item.goal as string) ?? `#${item.id}`}
        onGenerate={() => messageStrategy && generatePageStrategy(messageStrategy)}
        isGenerating={generatePageStrategyState.isLoading}
        generateLabel="Generuj page strategy"
        onDelete={(item) => deletePageStrategy({ id: item.id as number, messageStrategyId: id })}
      />
    </DetailShell>
  )
}
