import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetPageBlueprintQuery, useUpdatePageBlueprintMutation } from '@/features/pageBlueprint/pageBlueprintApi'
import {
  useDeletePageContentPlanMutation,
  useGeneratePageContentPlanMutation,
  useListPageContentPlanForPageBlueprintQuery,
} from '@/features/pageContentPlan/pageContentPlanApi'

export default function PageBlueprintDetailPage() {
  const id = Number(useParams().id)
  const { data: pageBlueprint, isLoading, error } = useGetPageBlueprintQuery(id)

  const list = useListPageContentPlanForPageBlueprintQuery(id)
  const [generate, generateState] = useGeneratePageContentPlanMutation()
  const [deletePageContentPlan] = useDeletePageContentPlanMutation()
  const [updatePageBlueprint, updateState] = useUpdatePageBlueprintMutation()

  return (
    <DetailShell
      title={(pageBlueprint?.page_type as string) ?? 'Page blueprint'}
      backTo={pageBlueprint ? `/page-requirements/${pageBlueprint.page_requirements_id}` : undefined}
      backLabel="← Page requirements"
      data={pageBlueprint}
      isLoading={isLoading}
      error={error}
      editable={{
        onSave: (fields) => updatePageBlueprint({ id, fields }).unwrap(),
        isSaving: updateState.isLoading,
      }}
    >
      <ResourceList
        title="Page content plan"
        items={list.data}
        isLoading={list.isLoading}
        error={list.error}
        linkTo={(item) => `/page-content-plan/${item.id}`}
        itemLabel={(item) => `#${item.id}`}
        onGenerate={() => generate(id)}
        isGenerating={generateState.isLoading}
        generateLabel="Generuj content plan"
        onDelete={(item) => deletePageContentPlan({ id: item.id as number, pageBlueprintId: id })}
      />
    </DetailShell>
  )
}
