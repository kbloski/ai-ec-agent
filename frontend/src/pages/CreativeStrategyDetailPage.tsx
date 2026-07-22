import type { FormEvent } from 'react'
import { Link, useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { Button } from '@/components/ui/button'
import { useGetCreativeStrategyQuery } from '@/features/creativeStrategy/creativeStrategyApi'
import {
  useCreateAdExecutionMutation,
  useDeleteAdExecutionMutation,
  useListAdExecutionForCreativeStrategyQuery,
} from '@/features/adExecution/adExecutionApi'

export default function CreativeStrategyDetailPage() {
  const id = Number(useParams().id)
  const { data: creativeStrategy, isLoading, error } = useGetCreativeStrategyQuery(id)

  const list = useListAdExecutionForCreativeStrategyQuery(id)
  const [createAdExecution, createState] = useCreateAdExecutionMutation()
  const [deleteAdExecution] = useDeleteAdExecutionMutation()

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    await createAdExecution({
      creativeStrategyId: id,
      name: String(formData.get('name') || '') || undefined,
      creative_type: String(formData.get('creative_type') || 'video'),
      platform: String(formData.get('platform') || 'Meta Ads'),
      format: String(formData.get('format') || 'Vertical Video 9:16'),
    }).unwrap()
  }

  return (
    <DetailShell
      title={(creativeStrategy?.name as string) ?? 'Creative strategy'}
      backTo={creativeStrategy ? `/ad-strategy/${creativeStrategy.ad_strategy_id}` : undefined}
      backLabel="← Ad strategy"
      data={creativeStrategy}
      isLoading={isLoading}
      error={error}
    >
      <section className="space-y-3 rounded-lg border p-4">
        <h2 className="text-lg font-semibold">Ad execution</h2>

        <form onSubmit={handleSubmit} className="flex flex-wrap items-end gap-2">
          <label className="text-xs">
            Nazwa
            <input name="name" className="block w-40 rounded-md border px-2 py-1 text-sm" />
          </label>
          <label className="text-xs">
            Typ kreacji
            <select
              name="creative_type"
              defaultValue="video"
              className="block w-32 rounded-md border px-2 py-1 text-sm"
            >
              <option value="video">video</option>
              <option value="image">image</option>
              <option value="carousel">carousel</option>
            </select>
          </label>
          <label className="text-xs">
            Platforma
            <input
              name="platform"
              defaultValue="Meta Ads"
              className="block w-40 rounded-md border px-2 py-1 text-sm"
            />
          </label>
          <label className="text-xs">
            Format
            <input
              name="format"
              defaultValue="Vertical Video 9:16"
              className="block w-48 rounded-md border px-2 py-1 text-sm"
            />
          </label>
          <Button type="submit" size="sm" disabled={createState.isLoading}>
            {createState.isLoading ? 'Tworzenie…' : 'Utwórz ad execution'}
          </Button>
        </form>

        {list.isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
        {Boolean(list.error) && <p className="text-sm text-destructive">Błąd pobierania.</p>}
        {!list.isLoading && !list.error && (list.data?.length ?? 0) === 0 && (
          <p className="text-sm text-muted-foreground">Brak elementów — wygeneruj pierwszy.</p>
        )}
        {(list.data?.length ?? 0) > 0 && (
          <ul className="-mx-4 divide-y border-t">
            {list.data?.map((item) => (
              <li key={item.id} className="flex items-center gap-2 px-4 py-2.5 hover:bg-accent/50">
                <Link to={`/ad-execution/${item.id}`} className="flex-1 truncate text-sm hover:underline">
                  {`#${item.id} ${(item.name as string) ?? ''}`.trim()}
                </Link>
                <Button
                  size="sm"
                  variant="black"
                  onClick={() => {
                    if (window.confirm('Czy na pewno usunąć ten element?')) {
                      deleteAdExecution({ id: item.id as number, creativeStrategyId: id })
                    }
                  }}
                >
                  Usuń
                </Button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </DetailShell>
  )
}
