import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { ResourceList } from '@/components/ResourceList'
import { useGetMarketingStrategyQuery } from '@/features/marketingStrategy/marketingStrategyApi'
import {
  useGenerateOfferStrategyMutation,
  useListOfferStrategyForMarketingStrategyQuery,
} from '@/features/offerStrategy/offerStrategyApi'

export default function MarketingStrategyDetailPage() {
  const id = Number(useParams().id)
  const { data: marketingStrategy, isLoading, error } = useGetMarketingStrategyQuery(id)

  const list = useListOfferStrategyForMarketingStrategyQuery(id)
  const [generate, generateState] = useGenerateOfferStrategyMutation()

  return (
    <DetailShell
      title="Marketing strategy"
      backTo={marketingStrategy ? `/brand-marketing/${marketingStrategy.brand_marketing_id}` : undefined}
      backLabel="← Brand marketing"
      data={marketingStrategy}
      isLoading={isLoading}
      error={error}
    >
      <ResourceList
        title="Offer strategy"
        items={list.data}
        isLoading={list.isLoading}
        error={list.error}
        linkTo={(item) => `/offer-strategy/${item.id}`}
        itemLabel={(item) => (item.offer_name as string) ?? `#${item.id}`}
        onGenerate={() => marketingStrategy && generate(marketingStrategy)}
        isGenerating={generateState.isLoading}
        generateLabel="Generuj offer strategy"
      />
    </DetailShell>
  )
}
