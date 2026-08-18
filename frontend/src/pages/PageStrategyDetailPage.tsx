import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetPageStrategyQuery, useUpdatePageStrategyMutation } from '@/features/pageStrategy/pageStrategyApi'
import {
  useCreatePageRequirementsMutation,
  useDeletePageRequirementsMutation,
  useListPageRequirementsForPageStrategyQuery,
} from '@/features/pageRequirements/pageRequirementsApi'

export default function PageStrategyDetailPage() {
  const id = Number(useParams().id)
  const { data: pageStrategy, isLoading, error } = useGetPageStrategyQuery(id)

  const list = useListPageRequirementsForPageStrategyQuery(id)
  const [create, createState] = useCreatePageRequirementsMutation()
  const [deletePageRequirements] = useDeletePageRequirementsMutation()
  const [updatePageStrategy, updateState] = useUpdatePageStrategyMutation()

  return (
    <DetailShell
      title={(pageStrategy?.goal as string) ?? 'Page strategy'}
      backTo={pageStrategy ? `/message-strategy/${pageStrategy.message_strategy_id}` : undefined}
      backLabel="← Message strategy"
      data={pageStrategy}
      isLoading={isLoading}
      error={error}
      editable={{
        onSave: (fields) => updatePageStrategy({ id, fields }).unwrap(),
        isSaving: updateState.isLoading,
      }}
    >
      <ResourceList
        title="Page requirements"
        items={list.data}
        isLoading={list.isLoading}
        error={list.error}
        linkTo={(item) => `/page-requirements/${item.id}`}
        itemLabel={(item) => `#${item.id}`}
        onGenerate={() => create(id)}
        isGenerating={createState.isLoading}
        generateLabel="Dodaj wymagania"
        onDelete={(item) => deletePageRequirements({ id: item.id as number, pageStrategyId: id })}
      />
    </DetailShell>
  )
}
