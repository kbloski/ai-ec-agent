import type { FormEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { ChevronDown } from 'lucide-react'
import { EntityViewer } from '@/components/EntityViewer'
import { useGetOfferItemQuery, useUpdateOfferItemMutation } from '@/features/offers/offersApi'

export default function OfferItemEditPage() {
  const id = Number(useParams().id)
  const navigate = useNavigate()

  const { data, isLoading, error } = useGetOfferItemQuery(id)
  const [updateOfferItem, updateState] = useUpdateOfferItemMutation()

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!data) return

    const formData = new FormData(e.currentTarget)

    await updateOfferItem({
      id,
      offerId: data.offer_id as number,
      fields: {
        name: String(formData.get('name') ?? ''),
        quantity: Number(formData.get('quantity') ?? 1),
        details: String(formData.get('details') ?? ''),
      },
    }).unwrap()

    navigate(`/offers/${data.offer_id}`)
  }

  return (
    <div className="mx-auto max-w-xl space-y-6 p-6">
      <h1 className="text-2xl font-semibold">Edytuj element oferty</h1>

      {data && (
        <Collapsible>
          <CollapsibleTrigger className="group flex items-center gap-1.5 text-xs font-medium tracking-wide text-muted-foreground uppercase hover:text-foreground">
            <ChevronDown className="size-3.5 shrink-0 transition-transform group-data-[panel-open]:rotate-180" />
            Pokaż surowy JSON
          </CollapsibleTrigger>
          <CollapsibleContent className="pt-2">
            <EntityViewer data={data} />
          </CollapsibleContent>
        </Collapsible>
      )}

      {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
      {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>}

      {data && (
        <form key={id} onSubmit={handleSubmit} className="space-y-4 rounded-lg border p-4">
          <div className="space-y-1">
            <Label htmlFor="name">Nazwa</Label>
            <Input id="name" name="name" defaultValue={(data.name as string) ?? ''} />
          </div>

          <div className="space-y-1">
            <Label htmlFor="quantity">Ilość</Label>
            <Input
              id="quantity"
              name="quantity"
              type="number"
              defaultValue={(data.quantity as number)?.toString() ?? '1'}
            />
          </div>

          <div className="space-y-1">
            <Label htmlFor="details">Szczegóły</Label>
            <Textarea id="details" name="details" defaultValue={(data.details as string) ?? ''} />
          </div>

          <div className="flex gap-2">
            <Button type="submit" disabled={updateState.isLoading}>
              {updateState.isLoading ? 'Zapisywanie…' : 'Zapisz'}
            </Button>
            <Button type="button" variant="black" onClick={() => navigate(`/offers/${data.offer_id}`)}>
              Anuluj
            </Button>
          </div>
        </form>
      )}
    </div>
  )
}
