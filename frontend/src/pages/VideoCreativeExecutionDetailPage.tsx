import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { useGetVideoCreativeExecutionQuery } from '@/features/videoCreativeExecution/videoCreativeExecutionApi'

export default function VideoCreativeExecutionDetailPage() {
  const id = Number(useParams().id)
  const { data, isLoading, error } = useGetVideoCreativeExecutionQuery(id)

  return (
    <DetailShell
      title="Video creative execution"
      backTo={data ? `/ad-execution/${data.ad_execution_id}` : undefined}
      backLabel="← Ad execution"
      data={data}
      isLoading={isLoading}
      error={error}
    />
  )
}
