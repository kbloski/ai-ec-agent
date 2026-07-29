import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import {
  useGetCreativeExecutionQuery,
  useUpdateCreativeExecutionMutation,
} from '@/features/creativeExecution/creativeExecutionApi'

export default function CreativeExecutionDetailPage() {
  const id = Number(useParams().id)
  const { data, isLoading, error } = useGetCreativeExecutionQuery(id)
  const [updateCreativeExecution, updateState] = useUpdateCreativeExecutionMutation()

  return (
    <DetailShell
      title="Creative execution"
      backTo={data ? `/ad-execution/${data.ad_execution_id}` : undefined}
      backLabel="← Ad execution"
      data={data}
      isLoading={isLoading}
      error={error}
      editable={{
        onSave: (fields) => updateCreativeExecution({ id, fields }).unwrap(),
        isSaving: updateState.isLoading,
      }}
    />
  )
}
