import { useState, type FormEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import {
  useGetTargetAudienceQuery,
  useUpdateTargetAudienceMutation,
  type UpdateTargetAudienceArgs,
} from '@/features/targetAudiences/targetAudiencesApi'
import { useListContentStatusesQuery } from '@/features/contentStatus/contentStatusApi'

const LIST_FIELDS = [
  'lifestyles',
  'values',
  'pain_points',
  'motivations',
  'buying_triggers',
  'objections',
  'message_angles',
  'marketing_channels',
] as const

const TEXT_FIELDS = [
  'name',
  'gender',
  'location',
  'purchasing_power',
  'awareness_level',
  'price_sensitivity',
  'research_level',
  'decision_time',
] as const

const NUMBER_FIELDS = ['score', 'confidence', 'age_min', 'age_max'] as const

function toLines(value: unknown): string {
  return Array.isArray(value) ? value.join('\n') : ''
}

function label(key: string): string {
  return key.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}

export default function TargetAudienceEditPage() {
  const id = Number(useParams().id)
  const navigate = useNavigate()

  const { data, isLoading, error } = useGetTargetAudienceQuery(id)
  const { data: statuses } = useListContentStatusesQuery()
  const [updateTargetAudience, updateState] = useUpdateTargetAudienceMutation()

  const [contentStatus, setContentStatus] = useState<string | undefined>(undefined)

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!data) return

    const formData = new FormData(e.currentTarget)

    const payload: Record<string, unknown> = { id }

    if (contentStatus) payload.content_status = contentStatus

    for (const field of TEXT_FIELDS) {
      const raw = formData.get(field)
      if (raw !== null) payload[field] = String(raw)
    }

    payload.reason = String(formData.get('reason') ?? '')

    for (const field of NUMBER_FIELDS) {
      const raw = formData.get(field)
      if (raw !== null && raw !== '') payload[field] = Number(raw)
    }

    for (const field of LIST_FIELDS) {
      const raw = String(formData.get(field) ?? '')
      payload[field] = raw
        .split('\n')
        .map((line) => line.trim())
        .filter(Boolean)
    }

    await updateTargetAudience(payload as UpdateTargetAudienceArgs).unwrap()

    navigate(`/target-audiences/${id}`)
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6 p-6">
      <h1 className="text-2xl font-semibold">Edytuj grupę docelową</h1>

      {isLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}
      {Boolean(error) && <p className="text-sm text-destructive">Nie udało się pobrać danych.</p>}

      {data && (
        <form key={id} onSubmit={handleSubmit} className="space-y-4 rounded-lg border p-4">
          <div className="space-y-1">
            <Label htmlFor="content_status">Status</Label>
            <Select
              value={contentStatus ?? (data.content_status as string)}
              onValueChange={setContentStatus}
            >
              <SelectTrigger id="content_status">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {statuses?.map((status) => (
                  <SelectItem key={status.value} value={status.value}>
                    {status.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {TEXT_FIELDS.map((field) => (
            <div key={field} className="space-y-1">
              <Label htmlFor={field}>{label(field)}</Label>
              <Input id={field} name={field} defaultValue={(data[field] as string) ?? ''} />
            </div>
          ))}

          <div className="space-y-1">
            <Label htmlFor="reason">Reason</Label>
            <Textarea id="reason" name="reason" defaultValue={(data.reason as string) ?? ''} />
          </div>

          <div className="grid grid-cols-2 gap-4">
            {NUMBER_FIELDS.map((field) => (
              <div key={field} className="space-y-1">
                <Label htmlFor={field}>{label(field)}</Label>
                <Input
                  id={field}
                  name={field}
                  type="number"
                  defaultValue={(data[field] as number | undefined)?.toString() ?? ''}
                />
              </div>
            ))}
          </div>

          {LIST_FIELDS.map((field) => (
            <div key={field} className="space-y-1">
              <Label htmlFor={field}>{label(field)} (jedna wartość na linię)</Label>
              <Textarea id={field} name={field} defaultValue={toLines(data[field])} rows={3} />
            </div>
          ))}

          <div className="flex gap-2">
            <Button type="submit" disabled={updateState.isLoading}>
              {updateState.isLoading ? 'Zapisywanie…' : 'Zapisz'}
            </Button>
            <Button type="button" variant="black" onClick={() => navigate(`/target-audiences/${id}`)}>
              Anuluj
            </Button>
          </div>
        </form>
      )}
    </div>
  )
}
