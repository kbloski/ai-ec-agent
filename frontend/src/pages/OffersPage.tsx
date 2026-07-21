import { useState, type FormEvent } from 'react'
import { z } from 'zod'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import {
  useCreateOfferMutation,
  useDeleteOfferMutation,
  useListOffersQuery,
} from '@/features/offers/offersApi'

const createOfferSchema = z.object({
  name: z.string().min(1, 'Nazwa jest wymagana'),
  buying_price: z.coerce.number().positive('Cena zakupu musi być dodatnia'),
  selling_price: z.coerce.number().positive().optional().or(z.literal('').transform(() => undefined)),
  details: z.string().optional(),
})

export default function OffersPage() {
  const { data, isLoading, error } = useListOffersQuery()
  const [createOffer, { isLoading: isCreating }] = useCreateOfferMutation()
  const [deleteOffer] = useDeleteOfferMutation()
  const [formError, setFormError] = useState<string | null>(null)

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setFormError(null)

    const formData = new FormData(e.currentTarget)
    const parsed = createOfferSchema.safeParse({
      name: formData.get('name'),
      buying_price: formData.get('buying_price'),
      selling_price: formData.get('selling_price'),
      details: formData.get('details'),
    })

    if (!parsed.success) {
      setFormError(parsed.error.issues[0]?.message ?? 'Nieprawidłowe dane')
      return
    }

    await createOffer(parsed.data).unwrap()
    e.currentTarget.reset()
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-6">
      <h1 className="text-2xl font-semibold">Oferty</h1>

      <form onSubmit={handleSubmit} className="space-y-2 rounded-lg border p-4">
        <h2 className="text-lg font-semibold">Nowa oferta</h2>
        <input
          name="name"
          placeholder="Nazwa"
          className="w-full rounded-md border px-3 py-2 text-sm"
        />
        <input
          name="buying_price"
          type="number"
          step="0.01"
          placeholder="Cena zakupu"
          className="w-full rounded-md border px-3 py-2 text-sm"
        />
        <input
          name="selling_price"
          type="number"
          step="0.01"
          placeholder="Cena sprzedaży (opcjonalnie)"
          className="w-full rounded-md border px-3 py-2 text-sm"
        />
        <textarea
          name="details"
          placeholder="Szczegóły (opcjonalnie)"
          className="w-full rounded-md border px-3 py-2 text-sm"
        />
        {formError && <p className="text-sm text-destructive">{formError}</p>}
        <Button type="submit" disabled={isCreating}>
          {isCreating ? 'Tworzenie…' : 'Utwórz ofertę'}
        </Button>
      </form>

      <section className="overflow-hidden rounded-lg border">
        {isLoading && <p className="px-4 py-3 text-sm text-muted-foreground">Ładowanie…</p>}
        {Boolean(error) && (
          <p className="px-4 py-3 text-sm text-destructive">Nie udało się pobrać ofert.</p>
        )}
        {!isLoading && !error && (data?.items.length ?? 0) === 0 && (
          <p className="px-4 py-3 text-sm text-muted-foreground">Brak ofert — utwórz pierwszą.</p>
        )}
        <ul className="divide-y">
          {data?.items.map((offer) => (
            <li key={offer.id} className="flex items-center gap-2 px-4 py-2.5 hover:bg-accent/50">
              <Link to={`/offers/${offer.id}`} className="flex-1 truncate text-sm hover:underline">
                {(offer.name as string) ?? `#${offer.id}`}
              </Link>
              <Button
                size="sm"
                variant="black"
                onClick={() => {
                  if (window.confirm('Czy na pewno usunąć tę ofertę?')) {
                    deleteOffer(offer.id as number)
                  }
                }}
              >
                Usuń
              </Button>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}
