import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { useGetAdExecutionQuery } from '@/features/adExecution/adExecutionApi'

export default function AdExecutionDetailPage() {
  const id = Number(useParams().id)
  const { data, isLoading, error } = useGetAdExecutionQuery(id)

  return (
    <DetailShell
      title={(data?.name as string) ?? 'Ad execution'}
      backTo={data ? `/creative-strategy/${data.creative_strategy_id}` : undefined}
      backLabel="← Creative strategy"
      data={data}
      isLoading={isLoading}
      error={error}
    />
  )
}
