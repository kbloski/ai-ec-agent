import { Link, useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { Button } from '@/components/ui/button'
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
    >
      <Button
        size="sm"
        variant="black"
        nativeButton={false}
        render={<Link to={`/target-audiences/${id}/edit`} />}
      >
        Edytuj
      </Button>
    </DetailShell>
  )
}
