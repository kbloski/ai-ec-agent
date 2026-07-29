import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { useGetPageCopyQuery, useUpdatePageCopyMutation } from '@/features/pageCopy/pageCopyApi'

export default function PageCopyDetailPage() {
  const id = Number(useParams().id)
  const { data, isLoading, error } = useGetPageCopyQuery(id)
  const [updatePageCopy, updateState] = useUpdatePageCopyMutation()

  return (
    <DetailShell
      title="Page copy"
      backTo={data ? `/page-content-plan/${data.page_content_plan_id}` : undefined}
      backLabel="← Page content plan"
      data={data}
      isLoading={isLoading}
      error={error}
      editable={{
        onSave: (fields) => updatePageCopy({ id, fields }).unwrap(),
        isSaving: updateState.isLoading,
      }}
    />
  )
}
