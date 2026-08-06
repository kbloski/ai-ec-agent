import { useState, type FormEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  useCreateOfferItemMutation,
  useDeleteOfferInsightMutation,
  useDeleteOfferItemMutation,
  useDeleteOfferMutation,
  useGenerateOfferSuggestionsMutation,
  useGetOfferQuery,
  useUpdateOfferInsightMutation,
  useUpdateOfferMutation,
} from '@/features/offers/offersApi'

export default function OfferDetailPage() {
  const offerId = Number(useParams().offerId)
  const navigate = useNavigate()
  const { data: offer, isLoading, error } = useGetOfferQuery(offerId)

  const [deleteOffer] = useDeleteOfferMutation()
  const [deleteOfferInsight] = useDeleteOfferInsightMutation()
  const [updateOfferInsight] = useUpdateOfferInsightMutation()
  const [deleteOfferItem] = useDeleteOfferItemMutation()
  const [createOfferItem, createOfferItemState] = useCreateOfferItemMutation()
  const [createItemError, setCreateItemError] = useState<string | null>(null)
  const [generateSuggestions, generateSuggestionsState] = useGenerateOfferSuggestionsMutation()
  const [updateOffer, updateOfferState] = useUpdateOfferMutation()

  const handleCreateItem = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setCreateItemError(null)

    const form = event.currentTarget
    const formData = new FormData(form)
    const name = String(formData.get('name') ?? '').trim()
    const quantity = Number(formData.get('quantity') ?? 1)

    if (!name) {
      setCreateItemError('Nazwa jest wymagana.')
      return
    }
    if (!Number.isInteger(quantity) || quantity < 1) {
      setCreateItemError('Ilość musi być liczbą całkowitą większą od zera.')
      return
    }

    try {
      await createOfferItem({
        offerId,
        name,
        quantity,
        details: String(formData.get('details') ?? '').trim() || undefined,
      }).unwrap()
      form.reset()
    } catch {
      setCreateItemError('Nie udało się dodać elementu oferty.')
    }
  }

  return (
    <DetailShell
      title={offer?.name as string}
      backTo="/offers"
      backLabel="← Oferty"
      data={offer}
      isLoading={isLoading}
      error={error}
      itemActions={{
        offer_insights: (item) => deleteOfferInsight({ id: item.id as number, offerId }),
        offer_items: (item) => deleteOfferItem({ id: item.id as number, offerId }),
      }}
      itemLinks={{
        offer_insights: (item) => `/offer-insights/${item.id}/edit`,
        offer_items: (item) => `/offer-items/${item.id}/edit`,
      }}
      relationLinks={{
        offer_insights: `/offers/${offerId}/insights`,
        offer_items: `/offers/${offerId}/items`,
      }}
      itemStatusActions={{
        offer_insights: (item, contentStatus) =>
          updateOfferInsight({
            id: item.id as number,
            offerId,
            content_status: contentStatus,
          }).unwrap(),
      }}
      itemAdditions={{
        offer_items: (
          <form onSubmit={handleCreateItem} className="space-y-3 rounded-md border p-3">
            <h3 className="text-sm font-semibold">Dodaj element oferty</h3>
            <div className="space-y-1">
              <Label htmlFor="new-offer-item-name">Nazwa</Label>
              <Input id="new-offer-item-name" name="name" required />
            </div>
            <div className="space-y-1">
              <Label htmlFor="new-offer-item-quantity">Ilość</Label>
              <Input
                id="new-offer-item-quantity"
                name="quantity"
                type="number"
                min="1"
                step="1"
                defaultValue="1"
                required
              />
            </div>
            <div className="space-y-1">
              <Label htmlFor="new-offer-item-details">Szczegóły</Label>
              <Textarea id="new-offer-item-details" name="details" />
            </div>
            {createItemError && <p className="text-sm text-destructive">{createItemError}</p>}
            <Button type="submit" size="sm" disabled={createOfferItemState.isLoading}>
              {createOfferItemState.isLoading ? 'Dodawanie…' : 'Dodaj element'}
            </Button>
          </form>
        ),
      }}
      editable={{
        onSave: (fields) => updateOffer({ id: offerId, fields }).unwrap(),
        isSaving: updateOfferState.isLoading,
      }}
      actions={
        <>
          <Button
            size="sm"
            variant="black"
            onClick={() => {
              if (window.confirm('Czy na pewno usunąć tę ofertę?')) {
                deleteOffer(offerId).then(() => navigate('/offers'))
              }
            }}
          >
            Usuń ofertę
          </Button>

          <Button
            size="sm"
            onClick={() => generateSuggestions(offerId)}
            disabled={generateSuggestionsState.isLoading}
          >
            {generateSuggestionsState.isLoading ? 'Generowanie…' : 'Generuj sugestie'}
          </Button>
        </>
      }
    />
  )
}
