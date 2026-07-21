import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetBrandMarketingQuery } from '@/features/brandMarketing/brandMarketingApi'
import {
  useDeleteMarketingStrategyMutation,
  useGenerateMarketingStrategyMutation,
  useListMarketingStrategyForBrandMarketingQuery,
} from '@/features/marketingStrategy/marketingStrategyApi'

export default function BrandMarketingDetailPage() {
  const id = Number(useParams().id)
  const { data: brandMarketing, isLoading, error } = useGetBrandMarketingQuery(id)

  const list = useListMarketingStrategyForBrandMarketingQuery(id)
  const [generate, generateState] = useGenerateMarketingStrategyMutation()
  const [deleteMarketingStrategy] = useDeleteMarketingStrategyMutation()

  return (
    <DetailShell
      title={(brandMarketing?.brand_name as string) ?? 'Brand marketing'}
      backTo={brandMarketing ? `/knowledges/${brandMarketing.knowledge_id}` : undefined}
      backLabel="← Knowledge"
      data={brandMarketing}
      isLoading={isLoading}
      error={error}
    >
      <ResourceList
        title="Marketing strategy"
        items={list.data}
        isLoading={list.isLoading}
        error={list.error}
        linkTo={(item) => `/marketing-strategy/${item.id}`}
        itemLabel={(item) => (item.marketing_objective as string) ?? `#${item.id}`}
        onGenerate={() => brandMarketing && generate(brandMarketing)}
        isGenerating={generateState.isLoading}
        generateLabel="Generuj marketing strategy"
        onDelete={(item) =>
          deleteMarketingStrategy({ id: item.id as number, brandMarketingId: id })
        }
      />
    </DetailShell>
  )
}
