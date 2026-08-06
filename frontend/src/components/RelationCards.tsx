import { ArrowRight } from 'lucide-react'
import { Link } from 'react-router-dom'

export interface RelationCard {
  id: string
  label: string
  count: number
  to: string
}

interface RelationCardsProps {
  cards: RelationCard[]
}

/** Summary cards that open the corresponding related-entities view. */
export function RelationCards({ cards }: RelationCardsProps) {
  if (cards.length === 0) return null

  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {cards.map((card) => (
        <Link
          key={card.id}
          to={card.to}
          className="group flex min-h-28 items-center justify-between rounded-lg border bg-card p-4 text-left transition-colors hover:border-foreground/40 hover:bg-accent/50"
        >
          <span>
            <span className="block text-3xl font-semibold tabular-nums">{card.count}</span>
            <span className="mt-1 block text-sm text-muted-foreground">{card.label}</span>
          </span>
          <ArrowRight className="size-5 text-muted-foreground transition-transform group-hover:translate-x-0.5 group-hover:text-foreground" />
        </Link>
      ))}
    </div>
  )
}
