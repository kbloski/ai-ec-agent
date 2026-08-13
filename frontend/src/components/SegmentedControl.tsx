import { useEffect, useState } from 'react'
import { cn } from '@/lib/utils'

interface SegmentedControlOption {
  value: string
  label: string
}

interface SegmentedControlProps {
  value?: string
  options?: SegmentedControlOption[]
  onValueChange: (value: string) => void | Promise<unknown>
  ariaLabel: string
  disabled?: boolean
}

export function SegmentedControl({
  value,
  options = [],
  onValueChange,
  ariaLabel,
  disabled = false,
}: SegmentedControlProps) {
  const [selectedValue, setSelectedValue] = useState(value)
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => setSelectedValue(value), [value])

  const select = async (nextValue: string) => {
    if (disabled || isSaving || nextValue === selectedValue) return

    const previousValue = selectedValue
    setSelectedValue(nextValue)
    setIsSaving(true)

    try {
      await onValueChange(nextValue)
    } catch {
      setSelectedValue(previousValue)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="flex flex-wrap gap-2" role="group" aria-label={ariaLabel} aria-busy={isSaving}>
      {options.map((option) => {
        const isSelected = option.value === selectedValue

        return (
          <button
            key={option.value}
            type="button"
            aria-pressed={isSelected}
            disabled={disabled || isSaving}
            onClick={() => void select(option.value)}
            className={cn(
              'flex min-h-7 cursor-pointer items-center gap-1.5 px-2 py-1 text-xs font-medium transition-colors',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/50',
              isSelected
                ? 'bg-muted font-bold text-foreground'
                : 'text-muted-foreground hover:bg-muted/70 hover:text-foreground',
              'disabled:cursor-wait disabled:opacity-60',
            )}
          >
            {option.label}
          </button>
        )
      })}
    </div>
  )
}
