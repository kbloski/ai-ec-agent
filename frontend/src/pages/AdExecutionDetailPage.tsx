import type { FormEvent } from 'react'
import { Link, useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { Button } from '@/components/ui/button'
import { useGetAdExecutionQuery, useUpdateAdExecutionMutation } from '@/features/adExecution/adExecutionApi'
import {
  useDeleteCreativeExecutionMutation,
  useGenerateCreativeExecutionMutation,
  useListCreativeExecutionForAdExecutionQuery,
} from '@/features/creativeExecution/creativeExecutionApi'
import { useListAdFrameworksQuery, type AdFramework } from '@/features/adFrameworks/adFrameworksApi'
import { useListCreativeAnglesQuery, type CreativeAngle } from '@/features/creativeAngels/creativeAnglesApi'

export default function AdExecutionDetailPage() {
  const id = Number(useParams().id)
  const { data, isLoading, error } = useGetAdExecutionQuery(id)

  const isVideo = data?.creative_type === 'video'
  const isImage = data?.creative_type === 'image'
  const isCarousel = data?.creative_type === 'carousel'
  const isGeneratable = isVideo || isImage || isCarousel

  const list = useListCreativeExecutionForAdExecutionQuery(id, { skip: !isGeneratable })
  const [generate, generateState] = useGenerateCreativeExecutionMutation()
  const [deleteCreativeExecution] = useDeleteCreativeExecutionMutation()
  const adFrameworks = useListAdFrameworksQuery()
  const creativeAngles = useListCreativeAnglesQuery()
  const [updateAdExecution, updateState] = useUpdateAdExecutionMutation()

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const durationRaw = formData.get('duration_seconds')
    const slidesRaw = formData.get('number_of_slides')
    const adFrameworkIdRaw = formData.get('ad_framework_id')
    const creativeAngleIdRaw = formData.get('creative_angle_id')

    await generate({
      adExecutionId: id,
      ...(durationRaw ? { duration_seconds: Number(durationRaw) } : {}),
      ...(slidesRaw ? { number_of_slides: Number(slidesRaw) } : {}),
      ...(adFrameworkIdRaw ? { ad_framework_id: String(adFrameworkIdRaw) } : {}),
      ...(creativeAngleIdRaw ? { creative_angle_id: String(creativeAngleIdRaw) } : {}),
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
      editable={{
        onSave: (fields) => updateAdExecution({ id, fields }).unwrap(),
        isSaving: updateState.isLoading,
      }}
    >
      {isGeneratable && (
        <section className="space-y-3 rounded-lg border p-4">
          <h2 className="text-lg font-semibold">Creative execution</h2>

          <form onSubmit={handleSubmit} className="flex flex-wrap items-end gap-2">
            <div className="space-y-1">
              <p className="text-xs font-semibold text-muted-foreground">Video</p>
              <label className="text-xs">
                Czas trwania (s)
                <input
                  name="duration_seconds"
                  type="number"
                  defaultValue={15}
                  disabled={!isVideo}
                  className="block w-28 rounded-md border px-2 py-1 text-sm disabled:opacity-50"
                />
              </label>
            </div>
            <div className="space-y-1">
              <p className="text-xs font-semibold text-muted-foreground">Carousel</p>
              <label className="text-xs">
                Liczba slajdów
                <input
                  name="number_of_slides"
                  type="number"
                  defaultValue={5}
                  disabled={!isCarousel}
                  className="block w-28 rounded-md border px-2 py-1 text-sm disabled:opacity-50"
                />
              </label>
            </div>
            <div className="space-y-1">
              <p className="text-xs font-semibold text-muted-foreground">Ad Framework</p>
              <label className="text-xs">
                Framework
                <select
                  name="ad_framework_id"
                  defaultValue=""
                  className="block w-40 rounded-md border px-2 py-1 text-sm"
                >
                  <option value="">—</option>
                  {adFrameworks.data?.map((framework: AdFramework) => (
                    <option key={framework.id} value={framework.id}>
                      {framework.name}
                    </option>
                  ))}
                </select>
              </label>
            </div>
            <div className="space-y-1">
              <p className="text-xs font-semibold text-muted-foreground">Creative Angle</p>
              <label className="text-xs">
                Angle
                <select
                  name="creative_angle_id"
                  defaultValue=""
                  className="block w-40 rounded-md border px-2 py-1 text-sm"
                >
                  <option value="">—</option>
                  {creativeAngles.data?.map((angle: CreativeAngle) => (
                    <option key={angle.id} value={angle.id}>
                      {angle.name}
                    </option>
                  ))}
                </select>
              </label>
            </div>
            <Button type="submit" size="sm" disabled={generateState.isLoading}>
              {generateState.isLoading ? 'Generowanie…' : 'Generuj creative execution'}
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
