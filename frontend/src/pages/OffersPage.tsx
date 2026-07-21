import { useState, type FormEvent } from 'react'
import { z } from 'zod'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { useCreateOfferMutation, useListOffersQuery } from '@/features/offers/offersApi'

const createOfferSchema = z.object({
  name: z.string().min(1, 'Nazwa jest wymagana'),
  buying_price: z.coerce.number().positive('Cena zakupu musi być dodatnia'),
  selling_price: z.coerce.number().positive().optional().or(z.literal('').transform(() => undefined)),
  details: z.string().optional(),
})

export default function OffersPage() {
  const { data, isLoading, error } = useListOffersQuery()
  const [createOffer, { isLoading: isCreating }] = useCreateOfferMutation()
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

      <section className="space-y-2">
        {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
        {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać ofert.</p>}
        <ul className="space-y-1">
          {data?.items.map((offer) => (
            <li key={offer.id}>
              <Link
                to={`/offers/${offer.id}`}
                className="block rounded-md border px-3 py-2 text-sm hover:bg-accent"
              >
                {(offer.name as string) ?? `#${offer.id}`}
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}
