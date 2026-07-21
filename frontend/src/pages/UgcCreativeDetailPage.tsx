import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { useGetUgcCreativeQuery } from '@/features/ugcCreatives/ugcCreativesApi'

export default function UgcCreativeDetailPage() {
  const id = Number(useParams().id)
  const { data, isLoading, error } = useGetUgcCreativeQuery(id)

  return (
    <DetailShell
      title={(data?.name as string) ?? 'UGC creative'}
      backTo={data ? `/message-strategy/${data.message_strategy_id}` : undefined}
      backLabel="← Message strategy"
      data={data}
      isLoading={isLoading}
      error={error}
    />
  )
}
