import { Plus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { EntityList } from '@/components/EntityList'
import type { Entity } from '@/types'

interface ResourceListProps {
  title: string
  items: Entity[] | undefined
  isLoading: boolean
  error?: unknown
  linkTo?: (item: Entity) => string
  itemLabel?: (item: Entity) => string
  onGenerate?: () => void
  isGenerating?: boolean
  generateLabel?: string
  onDelete?: (item: Entity) => void
}

/** Generic "list of children + generate new one" block reused by every pipeline stage page. */
export function ResourceList({
  title,
  items,
  isLoading,
  error,
  linkTo,
  itemLabel = (item) => (item.name as string) ?? `#${item.id}`,
  onGenerate,
  isGenerating,
  generateLabel = 'Generuj',
  onDelete,
}: ResourceListProps) {
  return (
    <EntityList
      title={title}
      items={items}
      isLoading={isLoading}
      error={error}
      linkTo={linkTo}
      itemLabel={itemLabel}
      onDelete={onDelete}
      emptyDescription="Wygeneruj lub dodaj pierwszy element, aby rozpocząć pracę."
      actions={onGenerate ? (
          <Button onClick={onGenerate} disabled={isGenerating} className="h-10 rounded-none px-4">
            <Plus />
            {isGenerating ? 'Generowanie…' : generateLabel}
          </Button>
      ) : undefined}
    />
  )
}
