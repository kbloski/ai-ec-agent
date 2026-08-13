import { useState, type FormEvent, type ReactNode } from 'react'
import { useParams } from 'react-router-dom'
import { RelationList } from '@/components/EditableFields'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { useListFactStatusesQuery } from '@/features/factStatus/factStatusApi'
import { useListReviewStatusesQuery } from '@/features/reviewStatus/reviewStatusApi'
import {
  useCreateOfferItemMutation,
  useDeleteOfferInsightMutation,
  useDeleteOfferItemMutation,
  useGetOfferQuery,
  useGenerateOfferSuggestionsMutation,
  useUpdateOfferInsightMutation,
} from '@/features/offers/offersApi'
import {
  useDeleteKnowledgeInsightMutation,
  useGetKnowledgeQuery,
  useUpdateKnowledgeInsightMutation,
} from '@/features/knowledge/knowledgeApi'
import {
  useDeleteTargetAudienceMutation,
  useGenerateTargetAudiencesMutation,
  useUpdateTargetAudienceMutation,
} from '@/features/targetAudiences/targetAudiencesApi'
import type { Entity } from '@/types'

function CollectionPage({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="w-full space-y-6 p-6 lg:p-10">
      <h1 className="text-2xl font-semibold">{title}</h1>
      {children}
    </div>
  )
}

export function OfferInsightsPage() {
  const offerId = Number(useParams().offerId)
  const { data, isLoading, error } = useGetOfferQuery(offerId)
  const { data: statuses } = useListFactStatusesQuery()
  const { data: reviewStatuses } = useListReviewStatusesQuery()
  const [remove] = useDeleteOfferInsightMutation()
  const [update] = useUpdateOfferInsightMutation()
  const [generateInsights, generateState] = useGenerateOfferSuggestionsMutation()
  const items = (data?.offer_insights as Entity[] | undefined) ?? []

  return (
    <CollectionPage title="Insights">
      <Button onClick={() => generateInsights(offerId)} disabled={generateState.isLoading}>
        {generateState.isLoading ? 'Generowanie…' : 'Generuj insights'}
      </Button>
      {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
      {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>}
      {!isLoading && !error && items.length === 0 && <p className="text-sm text-muted-foreground">Brak elementów.</p>}
      <RelationList fieldKey="offer_insights" items={items} onEditLink={(item) => `/offer-insights/${item.id}/edit`} onDelete={(item) => remove({ id: item.id as number, offerId })} onStatusChange={(item, fact_status) => update({ id: item.id as number, offerId, fact_status }).unwrap()} onReviewStatusChange={(item, review_status) => update({ id: item.id as number, offerId, review_status }).unwrap()} statuses={statuses} reviewStatuses={reviewStatuses} showHeading={false} />
    </CollectionPage>
  )
}

export function OfferItemsPage() {
  const offerId = Number(useParams().offerId)
  const { data, isLoading, error } = useGetOfferQuery(offerId)
  const [create, createState] = useCreateOfferItemMutation()
  const [remove] = useDeleteOfferItemMutation()
  const [formError, setFormError] = useState<string>()
  const items = (data?.offer_items as Entity[] | undefined) ?? []

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setFormError(undefined)
    const form = event.currentTarget
    const values = new FormData(form)
    const name = String(values.get('name') ?? '').trim()
    const quantity = Number(values.get('quantity') ?? 1)
    if (!name || !Number.isInteger(quantity) || quantity < 1) {
      setFormError('Podaj nazwę i poprawną ilość.')
      return
    }
    await create({ offerId, name, quantity, details: String(values.get('details') ?? '').trim() || undefined }).unwrap()
    form.reset()
  }

  return (
    <CollectionPage title="Elementy oferty">
      <form onSubmit={submit} className="space-y-3 bg-muted/25 p-4">
        <h2 className="font-semibold">Dodaj element oferty</h2>
        <div className="space-y-1"><Label htmlFor="item-name">Nazwa</Label><Input id="item-name" name="name" required /></div>
        <div className="space-y-1"><Label htmlFor="item-quantity">Ilość</Label><Input id="item-quantity" name="quantity" type="number" min="1" step="1" defaultValue="1" required /></div>
        <div className="space-y-1"><Label htmlFor="item-details">Szczegóły</Label><Textarea id="item-details" name="details" /></div>
        {formError && <p className="text-sm text-destructive">{formError}</p>}
        <Button type="submit" size="sm" disabled={createState.isLoading}>{createState.isLoading ? 'Dodawanie…' : 'Dodaj element'}</Button>
      </form>
      {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
      {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>}
      {!isLoading && !error && items.length === 0 && <p className="text-sm text-muted-foreground">Brak elementów.</p>}
      <RelationList fieldKey="offer_items" items={items} onEditLink={(item) => `/offer-items/${item.id}/edit`} onDelete={(item) => remove({ id: item.id as number, offerId })} showHeading={false} />
    </CollectionPage>
  )
}

export function KnowledgeInsightsPage() {
  const knowledgeId = Number(useParams().knowledgeId)
  const { data, isLoading, error } = useGetKnowledgeQuery(knowledgeId)
  const { data: statuses } = useListFactStatusesQuery()
  const { data: reviewStatuses } = useListReviewStatusesQuery()
  const [remove] = useDeleteKnowledgeInsightMutation()
  const [update] = useUpdateKnowledgeInsightMutation()
  const items = (data?.knowledge_insights as Entity[] | undefined) ?? []

  return <CollectionPage title="Insights">
    {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
    {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>}
    {!isLoading && !error && items.length === 0 && <p className="text-sm text-muted-foreground">Brak elementów.</p>}
    <RelationList fieldKey="knowledge_insights" items={items} onEditLink={(item) => `/knowledge-insights/${item.id}/edit`} onDelete={(item) => remove({ id: item.id as number, knowledgeId })} onStatusChange={(item, fact_status) => update({ id: item.id as number, knowledgeId, fact_status }).unwrap()} onReviewStatusChange={(item, review_status) => update({ id: item.id as number, knowledgeId, review_status }).unwrap()} statuses={statuses} reviewStatuses={reviewStatuses} showHeading={false} />
  </CollectionPage>
}

export function KnowledgeTargetAudiencesPage() {
  const knowledgeId = Number(useParams().knowledgeId)
  const { data, isLoading, error } = useGetKnowledgeQuery(knowledgeId)
  const { data: statuses } = useListFactStatusesQuery()
  const { data: reviewStatuses } = useListReviewStatusesQuery()
  const [generate, generateState] = useGenerateTargetAudiencesMutation()
  const [remove] = useDeleteTargetAudienceMutation()
  const [update] = useUpdateTargetAudienceMutation()
  const items = (data?.target_audiences as Entity[] | undefined) ?? []

  return <CollectionPage title="Grupy docelowe">
    <Button size="sm" onClick={() => generate({ knowledgeId })} disabled={generateState.isLoading}>{generateState.isLoading ? 'Generowanie…' : 'Generuj grupy docelowe'}</Button>
    {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
    {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>}
    {!isLoading && !error && items.length === 0 && <p className="text-sm text-muted-foreground">Brak elementów.</p>}
    <RelationList fieldKey="target_audiences" items={items} onEditLink={(item) => `/target-audiences/${item.id}/edit`} onDelete={(item) => remove({ id: item.id as number, knowledgeId })} onStatusChange={(item, fact_status) => update({ id: item.id as number, knowledgeId, fact_status }).unwrap()} onReviewStatusChange={(item, review_status) => update({ id: item.id as number, knowledgeId, review_status }).unwrap()} statuses={statuses} reviewStatuses={reviewStatuses} showHeading={false} />
  </CollectionPage>
}
