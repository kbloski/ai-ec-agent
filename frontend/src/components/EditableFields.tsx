import { useState, type FormEvent } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { RelationList } from '@/components/EntityFields'
import { isPrimitive, isRelationArray, label } from '@/lib/entityFields'
import { useListContentStatusesQuery } from '@/features/contentStatus/contentStatusApi'

const SKIP_KEYS = new Set(['id', 'created_at', 'updated_at'])

function isSkipped(key: string): boolean {
  return SKIP_KEYS.has(key) || (key.endsWith('_id') && key !== 'id')
}

function toFormValue(value: unknown): string {
  if (value === null || value === undefined) return ''
  if (isPrimitive(value)) return String(value)
  return JSON.stringify(value, null, 2)
}

interface EditableFieldsProps {
  data: Record<string, unknown>
  onSave: (fields: Record<string, unknown>) => Promise<void>
  isSaving?: boolean
  itemActions?: Record<string, (item: Record<string, unknown>) => void>
  itemLinks?: Record<string, (item: Record<string, unknown>) => string>
}

/** Editable counterpart to EntityFields — same field-type detection, but with inputs instead of read-only text. Relation arrays (child entities with their own `id`) stay read-only, rendered via RelationList. */
export function EditableFields({
  data,
  onSave,
  isSaving,
  itemActions,
  itemLinks,
}: EditableFieldsProps) {
  const { data: statuses } = useListContentStatusesQuery()

  const editableKeys = Object.keys(data).filter(
    (key) => !isSkipped(key) && !isRelationArray(data[key])
  )
  const relationKeys = Object.keys(data).filter(
    (key) => !isSkipped(key) && isRelationArray(data[key])
  )

  const [values, setValues] = useState<Record<string, string>>(() =>
    Object.fromEntries(editableKeys.map((key) => [key, toFormValue(data[key])]))
  )
  const [error, setError] = useState<string | null>(null)

  const setField = (key: string, value: string) =>
    setValues((prev) => ({ ...prev, [key]: value }))

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError(null)

    const fields: Record<string, unknown> = {}

    for (const key of editableKeys) {
      const original = data[key]
      const raw = values[key]

      if (key === 'content_status') {
        fields[key] = raw
      } else if (typeof original === 'number') {
        fields[key] = raw === '' ? null : Number(raw)
      } else if ((original === null || original === undefined) && raw === '') {
        fields[key] = null
      } else if (isPrimitive(original) || original === null || original === undefined) {
        fields[key] = raw
      } else {
        try {
          fields[key] = raw.trim() === '' ? null : JSON.parse(raw)
        } catch {
          setError(`Nieprawidłowy JSON w polu "${label(key)}"`)
          return
        }
      }
    }

    await onSave(fields)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <p className="text-sm text-destructive">{error}</p>}

      <div className="space-y-3">
        {editableKeys.map((key) => (
          <div key={key} className="space-y-1">
            <Label htmlFor={key}>{label(key)}</Label>
            {key === 'content_status' ? (
              <Select value={values[key]} onValueChange={(v) => setField(key, v)}>
                <SelectTrigger id={key}>
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
            ) : typeof data[key] === 'number' ? (
              <Input
                id={key}
                type="number"
                value={values[key]}
                onChange={(e) => setField(key, e.target.value)}
              />
            ) : (
              <Textarea
                id={key}
                value={values[key]}
                onChange={(e) => setField(key, e.target.value)}
                rows={typeof data[key] === 'string' && (data[key] as string).length > 80 ? 4 : 2}
              />
            )}
          </div>
        ))}
      </div>

      {relationKeys.length > 0 && (
        <div className="space-y-3">
          {relationKeys.map((key) => (
            <RelationList
              key={key}
              fieldKey={key}
              items={data[key] as Record<string, unknown>[]}
              onDelete={itemActions?.[key]}
              onEditLink={itemLinks?.[key]}
            />
          ))}
        </div>
      )}

      <div className="flex gap-2">
        <Button type="submit" disabled={isSaving}>
          {isSaving ? 'Zapisywanie…' : 'Zapisz'}
        </Button>
      </div>
    </form>
  )
}
