const LABEL_OVERRIDES: Record<string, string> = {
  id: 'ID',
  cta: 'CTA',
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

    return (
      <div className="space-y-2">
        {value.map((item, i) => (
          <div key={i} className="rounded-md border p-3">
            <EntityFields data={item as Record<string, unknown>} />
          </div>
        ))}
      </div>
    )
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
export function EntityFields({ data }: { data: Record<string, unknown> }) {
  const entries = Object.entries(data).filter(([key]) => key !== 'id')

  return (
    <dl className="space-y-3">
      {entries.map(([key, value]) => (
        <div key={key} className="grid gap-1">
          <dt className="text-xs font-medium tracking-wide text-muted-foreground uppercase">
            {label(key)}
          </dt>
          <dd className="text-sm">
            <Value value={value} />
          </dd>
        </div>
      ))}
    </dl>
  )
}
