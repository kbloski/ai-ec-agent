import { ChevronDown } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { Button } from '@/components/ui/button'
import { isPrimitive, label } from '@/lib/entityFields'

function ObjectArray({
  items,
  onDelete,
  onEditLink,
}: {
  items: Record<string, unknown>[]
  onDelete?: (item: Record<string, unknown>) => void
  onEditLink?: (item: Record<string, unknown>) => string
}) {
  return (
    <div className="space-y-2">
      {items.map((item, i) => (
        <div key={i} className="space-y-2 rounded-md border p-3">
          {(onDelete || onEditLink) && (
            <div className="flex justify-end gap-2">
              {onEditLink && (
                <Button
                  size="sm"
                  variant="black"
                  nativeButton={false}
                  render={<Link to={onEditLink(item)} />}
                >
                  Edytuj
                </Button>
              )}
              {onDelete && (
                <Button
                  size="sm"
                  variant="black"
                  onClick={() => {
                    if (window.confirm('Czy na pewno usunąć ten element?')) {
                      onDelete(item)
                    }
                  }}
                >
                  Usuń
                </Button>
              )}
            </div>
          )}
          <EntityFields data={item} />
        </div>
      ))}
    </div>
  )
}

/** Labeled, collapsible list of a relation field's items (each with its own "id"), with optional per-item "Edytuj"/"Usuń" actions. */
export function RelationList({
  fieldKey,
  items,
  onDelete,
  onEditLink,
}: {
  fieldKey: string
  items: Record<string, unknown>[]
  onDelete?: (item: Record<string, unknown>) => void
  onEditLink?: (item: Record<string, unknown>) => string
}) {
  if (items.length === 0) return null

  return (
    <Collapsible>
      <CollapsibleTrigger className="group flex items-center gap-1.5 text-xs font-medium tracking-wide text-muted-foreground uppercase hover:text-foreground">
        <ChevronDown className="size-3.5 shrink-0 transition-transform group-data-[panel-open]:rotate-180" />
        {label(fieldKey)} ({items.length})
      </CollapsibleTrigger>
      <CollapsibleContent className="pt-2">
        <ObjectArray items={items} onDelete={onDelete} onEditLink={onEditLink} />
      </CollapsibleContent>
    </Collapsible>
  )
}

function Value({ value }: { value: unknown }) {
  if (value === null || value === undefined || value === '') {
    return <span className="text-muted-foreground italic">—</span>
  }

  if (isPrimitive(value)) {
    return <span className="whitespace-pre-wrap">{String(value)}</span>
  }

  if (Array.isArray(value)) {
    if (value.length === 0) {
      return <span className="text-muted-foreground italic">—</span>
    }

    if (value.every(isPrimitive)) {
      return (
        <ul className="list-disc space-y-1 pl-5">
          {value.map((item, i) => (
            <li key={i}>{String(item)}</li>
          ))}
        </ul>
      )
    }

    return <ObjectArray items={value as Record<string, unknown>[]} />
  }

  if (typeof value === 'object') {
    return (
      <div className="rounded-md border p-3">
        <EntityFields data={value as Record<string, unknown>} />
      </div>
    )
  }

  return <span>{String(value)}</span>
}

/** Generically renders any DTO's fields — no per-resource forms needed since nothing here is user-editable. */
export function EntityFields({
  data,
  exclude = [],
  collapsibleFields = [],
  itemActions = {},
  itemLinks = {},
}: {
  data: Record<string, unknown>
  exclude?: string[]
  /** Array-of-objects fields rendered as a collapsed-by-default dropdown instead of always expanded. */
  collapsibleFields?: string[]
  /** Per-field delete handler for items of a collapsible array field, keyed by field name. */
  itemActions?: Record<string, (item: Record<string, unknown>) => void>
  /** Per-field "Edytuj" link target for items of a collapsible array field, keyed by field name. */
  itemLinks?: Record<string, (item: Record<string, unknown>) => string>
}) {
  const entries = Object.entries(data).filter(([key]) => key !== 'id' && !exclude.includes(key))

  return (
    <dl className="space-y-3">
      {entries.map(([key, value]) => {
        const asCollapsible =
          collapsibleFields.includes(key) && Array.isArray(value) && value.length > 0

        if (asCollapsible) {
          return (
            <RelationList
              key={key}
              fieldKey={key}
              items={value as Record<string, unknown>[]}
              onDelete={itemActions[key]}
              onEditLink={itemLinks[key]}
            />
          )
        }

        return (
          <div key={key} className="grid gap-1">
            <dt className="text-xs font-medium tracking-wide text-muted-foreground uppercase">
              {label(key)}
            </dt>
            <dd className="text-sm">
              <Value value={value} />
            </dd>
          </div>
        )
      })}
    </dl>
  )
}
