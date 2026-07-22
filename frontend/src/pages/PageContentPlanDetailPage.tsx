import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetPageContentPlanQuery } from '@/features/pageContentPlan/pageContentPlanApi'
import {
  useDeletePageCopyMutation,
  useGeneratePageCopyMutation,
  useListPageCopyForPageContentPlanQuery,
} from '@/features/pageCopy/pageCopyApi'

export default function PageContentPlanDetailPage() {
  const id = Number(useParams().id)
  const { data: pageContentPlan, isLoading, error } = useGetPageContentPlanQuery(id)

  const list = useListPageCopyForPageContentPlanQuery(id)
  const [generate, generateState] = useGeneratePageCopyMutation()
  const [deletePageCopy] = useDeletePageCopyMutation()

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
        onGenerate={() => generate(id)}
        isGenerating={generateState.isLoading}
        generateLabel="Generuj page copy"
        onDelete={(item) => deletePageCopy({ id: item.id as number, pageContentPlanId: id })}
      />
    </DetailShell>
  )
}
