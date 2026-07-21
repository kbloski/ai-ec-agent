import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetPageContentPlanQuery } from '@/features/pageContentPlan/pageContentPlanApi'
import { useGetPageBlueprintQuery } from '@/features/pageBlueprint/pageBlueprintApi'
import { useGetPageStrategyQuery } from '@/features/pageStrategy/pageStrategyApi'
import { useGetMessageStrategyQuery } from '@/features/messageStrategy/messageStrategyApi'
import {
  useGeneratePageCopyMutation,
  useListPageCopyForPageContentPlanQuery,
} from '@/features/pageCopy/pageCopyApi'

export default function PageContentPlanDetailPage() {
  const id = Number(useParams().id)
  const { data: pageContentPlan, isLoading, error } = useGetPageContentPlanQuery(id)

  const { data: pageBlueprint } = useGetPageBlueprintQuery(
    pageContentPlan?.page_blueprint_id as number,
    { skip: !pageContentPlan },
  )
  const { data: pageStrategy } = useGetPageStrategyQuery(
    pageBlueprint?.page_strategy_id as number,
    { skip: !pageBlueprint },
  )
  const { data: messageStrategy } = useGetMessageStrategyQuery(
    pageStrategy?.message_strategy_id as number,
    { skip: !pageStrategy },
  )

  const list = useListPageCopyForPageContentPlanQuery(id)
  const [generate, generateState] = useGeneratePageCopyMutation()

  return (
    <DetailShell
      title="Page content plan"
      backTo={pageContentPlan ? `/page-blueprint/${pageContentPlan.page_blueprint_id}` : undefined}
      backLabel="← Page blueprint"
      data={pageContentPlan}
      isLoading={isLoading}
      error={error}
    >
      <ResourceList
        title="Page copy"
        items={list.data}
        isLoading={list.isLoading}
        error={list.error}
        linkTo={(item) => `/page-copy/${item.id}`}
        itemLabel={(item) => `#${item.id}`}
        onGenerate={() =>
          messageStrategy &&
          pageBlueprint &&
          generate({
            chain: messageStrategy,
            pageStrategyId: pageBlueprint.page_strategy_id as number,
            pageBlueprintId: pageBlueprint.id,
            pageContentPlanId: id,
          })
        }
        isGenerating={generateState.isLoading}
        generateLabel="Generuj page copy"
      />
    </DetailShell>
  )
}
