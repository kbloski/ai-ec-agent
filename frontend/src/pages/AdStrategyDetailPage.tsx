import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetAdStrategyQuery } from '@/features/adStrategy/adStrategyApi'
import {
  useGenerateCreativeStrategyMutation,
  useListCreativeStrategyForAdStrategyQuery,
} from '@/features/creativeStrategy/creativeStrategyApi'

export default function AdStrategyDetailPage() {
  const id = Number(useParams().id)
  const { data: adStrategy, isLoading, error } = useGetAdStrategyQuery(id)

  const list = useListCreativeStrategyForAdStrategyQuery(id)
  const [generate, generateState] = useGenerateCreativeStrategyMutation()

  return (
    <DetailShell
      title="Ad strategy"
      backTo={adStrategy ? `/message-strategy/${adStrategy.message_strategy_id}` : undefined}
      backLabel="← Message strategy"
      data={adStrategy}
      isLoading={isLoading}
      error={error}
    >
      <ResourceList
        title="Creative strategy"
        items={list.data}
        isLoading={list.isLoading}
        error={list.error}
        linkTo={(item) => `/creative-strategy/${item.id}`}
        itemLabel={(item) => (item.name as string) ?? `#${item.id}`}
        onGenerate={() => adStrategy && generate(adStrategy)}
        isGenerating={generateState.isLoading}
        generateLabel="Generuj creative strategy"
      />
    </DetailShell>
  )
}
