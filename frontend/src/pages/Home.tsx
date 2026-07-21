import { Button } from '@/components/ui/button'
import { useGetOffersQuery } from '@/features/offers/offersApi'

export default function Home() {
  const { data: offers, isLoading, error } = useGetOffersQuery()

  return (
    <section className="mx-auto flex max-w-2xl flex-col items-start gap-4 p-8">
      <h1 className="text-3xl font-semibold">Home</h1>
      <p className="text-muted-foreground">
        {isLoading && 'Loading offers…'}
        {error && 'Failed to reach the backend API.'}
        {offers && `Backend connected — ${offers.items.length} offer(s) loaded.`}
      </p>
      <Button>Example button</Button>
    </section>
  )
}
