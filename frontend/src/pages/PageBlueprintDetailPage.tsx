import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetPageBlueprintQuery } from '@/features/pageBlueprint/pageBlueprintApi'
import { useGetPageStrategyQuery } from '@/features/pageStrategy/pageStrategyApi'
import { useGetMessageStrategyQuery } from '@/features/messageStrategy/messageStrategyApi'
import {
  useGeneratePageContentPlanMutation,
  useListPageContentPlanForPageBlueprintQuery,
} from '@/features/pageContentPlan/pageContentPlanApi'

export default function PageBlueprintDetailPage() {
  const id = Number(useParams().id)
  const { data: pageBlueprint, isLoading, error } = useGetPageBlueprintQuery(id)

  const { data: pageStrategy } = useGetPageStrategyQuery(
    pageBlueprint?.page_strategy_id as number,
    { skip: !pageBlueprint },
  )
  const { data: messageStrategy } = useGetMessageStrategyQuery(
    pageStrategy?.message_strategy_id as number,
    { skip: !pageStrategy },
  )

  const list = useListPageContentPlanForPageBlueprintQuery(id)
  const [generate, generateState] = useGeneratePageContentPlanMutation()

  return (
    <DetailShell
      title={(pageBlueprint?.page_type as string) ?? 'Page blueprint'}
      backTo={pageBlueprint ? `/page-strategy/${pageBlueprint.page_strategy_id}` : undefined}
      backLabel="← Page strategy"
      data={pageBlueprint}
      isLoading={isLoading}
      error={error}
    >
      <ResourceList
        title="Page content plan"
        items={list.data}
        isLoading={list.isLoading}
        error={list.error}
        linkTo={(item) => `/page-content-plan/${item.id}`}
        itemLabel={(item) => `#${item.id}`}
        onGenerate={() =>
          messageStrategy &&
          generate({
            chain: messageStrategy,
            pageStrategyId: pageBlueprint!.page_strategy_id as number,
            pageBlueprintId: id,
          })
        }
        isGenerating={generateState.isLoading}
        generateLabel="Generuj content plan"
      />
    </DetailShell>
  )
}
