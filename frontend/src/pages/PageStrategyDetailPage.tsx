import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetPageStrategyQuery } from '@/features/pageStrategy/pageStrategyApi'
import { useGetMessageStrategyQuery } from '@/features/messageStrategy/messageStrategyApi'
import {
  useGeneratePageBlueprintMutation,
  useListPageBlueprintForPageStrategyQuery,
} from '@/features/pageBlueprint/pageBlueprintApi'

export default function PageStrategyDetailPage() {
  const id = Number(useParams().id)
  const { data: pageStrategy, isLoading, error } = useGetPageStrategyQuery(id)

  // Needed to reconstruct the full ancestor chain (page_strategy DTO only stores message_strategy_id).
  const { data: messageStrategy } = useGetMessageStrategyQuery(
    pageStrategy?.message_strategy_id as number,
    { skip: !pageStrategy },
  )

  const list = useListPageBlueprintForPageStrategyQuery(id)
  const [generate, generateState] = useGeneratePageBlueprintMutation()

  return (
    <DetailShell
      title={(pageStrategy?.goal as string) ?? 'Page strategy'}
      backTo={pageStrategy ? `/message-strategy/${pageStrategy.message_strategy_id}` : undefined}
      backLabel="← Message strategy"
      data={pageStrategy}
      isLoading={isLoading}
      error={error}
    >
      <ResourceList
        title="Page blueprint"
        items={list.data}
        isLoading={list.isLoading}
        error={list.error}
        linkTo={(item) => `/page-blueprint/${item.id}`}
        itemLabel={(item) => (item.page_type as string) ?? `#${item.id}`}
        onGenerate={() =>
          messageStrategy && generate({ chain: messageStrategy, pageStrategyId: id })
        }
        isGenerating={generateState.isLoading}
        generateLabel="Generuj page blueprint"
      />
    </DetailShell>
  )
}
