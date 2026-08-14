import { cn } from '@/lib/utils'

interface MultiToggleOption {
  value: string
  label: string
}

interface MultiToggleProps {
  values: string[]
  options?: MultiToggleOption[]
  onValueChange: (values: string[]) => void
  ariaLabel: string
  disabled?: boolean
}

export function MultiToggle({
  values,
  options = [],
  onValueChange,
  ariaLabel,
  disabled = false,
}: MultiToggleProps) {
  const toggle = (optionValue: string) => {
    if (disabled) return

    const next = values.includes(optionValue)
      ? values.filter((value) => value !== optionValue)
      : [...values, optionValue]

    onValueChange(next)
  }

  return (
    <div className="flex flex-wrap gap-2" role="group" aria-label={ariaLabel}>
      {options.map((option) => {
        const isSelected = values.includes(option.value)

        return (
          <button
            key={option.value}
            type="button"
            aria-pressed={isSelected}
            disabled={disabled}
            onClick={() => toggle(option.value)}
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
