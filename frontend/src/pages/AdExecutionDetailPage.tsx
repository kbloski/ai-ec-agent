import type { FormEvent } from 'react'
import { Link, useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { Button } from '@/components/ui/button'
import { useGetAdExecutionQuery } from '@/features/adExecution/adExecutionApi'
import {
  useDeleteCreativeExecutionMutation,
  useGenerateCreativeExecutionMutation,
  useListCreativeExecutionForAdExecutionQuery,
} from '@/features/creativeExecution/creativeExecutionApi'

export default function AdExecutionDetailPage() {
  const id = Number(useParams().id)
  const { data, isLoading, error } = useGetAdExecutionQuery(id)

  const isVideo = data?.creative_type === 'video'

  const list = useListCreativeExecutionForAdExecutionQuery(id, { skip: !isVideo })
  const [generate, generateState] = useGenerateCreativeExecutionMutation()
  const [deleteCreativeExecution] = useDeleteCreativeExecutionMutation()

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    await generate({
      adExecutionId: id,
      duration_seconds: Number(formData.get('duration_seconds')) || 15,
    }).unwrap()
  }

  return (
    <DetailShell
      title={(data?.name as string) ?? 'Ad execution'}
      backTo={data ? `/creative-strategy/${data.creative_strategy_id}` : undefined}
      backLabel="← Creative strategy"
      data={data}
      isLoading={isLoading}
      error={error}
    >
      {isVideo && (
        <section className="space-y-3 rounded-lg border p-4">
          <h2 className="text-lg font-semibold">Creative execution</h2>

          <form onSubmit={handleSubmit} className="flex flex-wrap items-end gap-2">
            <label className="text-xs">
              Czas trwania (s)
              <input
                name="duration_seconds"
                type="number"
                defaultValue={15}
                className="block w-28 rounded-md border px-2 py-1 text-sm"
              />
            </label>
            <Button type="submit" size="sm" disabled={generateState.isLoading}>
              {generateState.isLoading ? 'Generowanie…' : 'Generuj video creative execution'}
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
                  <Link
                    to={`/creative-execution/${item.id}`}
                    className="flex-1 truncate text-sm hover:underline"
                  >
                    {`#${item.id}`}
                  </Link>
                  <Button
                    size="sm"
                    variant="black"
                    onClick={() => {
                      if (window.confirm('Czy na pewno usunąć ten element?')) {
                        deleteCreativeExecution({ id: item.id as number, adExecutionId: id })
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
      )}
    </DetailShell>
  )
}
