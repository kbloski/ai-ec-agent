import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { useGetTargetAudienceQuery } from '@/features/targetAudiences/targetAudiencesApi'

export default function TargetAudienceDetailPage() {
  const id = Number(useParams().id)
  const { data, isLoading, error } = useGetTargetAudienceQuery(id)

  return (
    <DetailShell
      title={(data?.name as string) ?? 'Grupa docelowa'}
      backTo={data ? `/knowledges/${data.knowledge_id}` : undefined}
      backLabel="← Knowledge"
      data={data}
      isLoading={isLoading}
      error={error}
    />
  )
}
