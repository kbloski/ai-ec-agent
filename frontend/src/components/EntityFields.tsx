import { ChevronDown } from 'lucide-react'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'

const LABEL_OVERRIDES: Record<string, string> = {
  id: 'ID',
  cta: 'CTA',
  offer_items: 'Elementy oferty',
  offer_insights: 'Insights',
  target_audiences: 'Grupy docelowe',
}

function label(key: string): string {
  if (LABEL_OVERRIDES[key]) return LABEL_OVERRIDES[key]
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase())
}

function isPrimitive(value: unknown): value is string | number | boolean {
  return (
    typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean'
  )
}

function ObjectArray({ items }: { items: Record<string, unknown>[] }) {
  return (
    <div className="space-y-2">
      {items.map((item, i) => (
        <div key={i} className="rounded-md border p-3">
          <EntityFields data={item} />
        </div>
      ))}
    </div>
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
}: {
  data: Record<string, unknown>
  exclude?: string[]
  /** Array-of-objects fields rendered as a collapsed-by-default dropdown instead of always expanded. */
  collapsibleFields?: string[]
}) {
  const entries = Object.entries(data).filter(([key]) => key !== 'id' && !exclude.includes(key))

  return (
    <dl className="space-y-3">
      {entries.map(([key, value]) => {
        const asCollapsible =
          collapsibleFields.includes(key) && Array.isArray(value) && value.length > 0

        if (asCollapsible) {
          return (
            <Collapsible key={key}>
              <CollapsibleTrigger className="group flex items-center gap-1.5 text-xs font-medium tracking-wide text-muted-foreground uppercase hover:text-foreground">
                <ChevronDown className="size-3.5 shrink-0 transition-transform group-data-[panel-open]:rotate-180" />
                {label(key)} ({(value as unknown[]).length})
              </CollapsibleTrigger>
              <CollapsibleContent className="pt-2">
                <ObjectArray items={value as Record<string, unknown>[]} />
              </CollapsibleContent>
            </Collapsible>
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
