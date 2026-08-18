import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { DetailShell } from '@/components/DetailShell'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import {
  useGetPageRequirementsQuery,
  useUpdatePageRequirementsMutation,
} from '@/features/pageRequirements/pageRequirementsApi'
import { useListPageSectionsQuery } from '@/features/pageSections/pageSectionsApi'

const REQUIREMENT_OPTIONS = [
  { value: 'required', label: 'Wymagana' },
  { value: 'optional', label: 'Opcjonalna' },
  { value: 'excluded', label: 'Wykluczona' },
]

interface SectionState {
  requirement_type?: string
  position?: string
}

interface PageSectionRequirement {
  page_section_type_id: string
  requirement_type: string
  position: number | null
}

export default function PageRequirementsDetailPage() {
  const id = Number(useParams().id)
  const { data: pageRequirements, isLoading, error } = useGetPageRequirementsQuery(id)
  const { data: sectionTypes, isLoading: sectionsLoading } = useListPageSectionsQuery()

  const [updatePageRequirements, updateState] = useUpdatePageRequirementsMutation()

  const [values, setValues] = useState<Record<string, SectionState>>({})

  useEffect(() => {
    const sectionRequirements =
      (pageRequirements?.page_section_requirements as PageSectionRequirement[] | undefined) ?? []

    setValues(
      Object.fromEntries(
        sectionRequirements.map((item) => [
          item.page_section_type_id,
          {
            requirement_type: item.requirement_type,
            position: item.position == null ? '' : String(item.position),
          },
        ]),
      ),
    )
  }, [pageRequirements])

  const setSectionValue = (sectionType: string, patch: Partial<SectionState>) =>
    setValues((prev) => ({ ...prev, [sectionType]: { ...prev[sectionType], ...patch } }))

  const handleSave = () => {
    const sectionRequirements = Object.entries(values)
      .filter(([, value]) => value.requirement_type)
      .map(([page_section_type_id, value]) => ({
        page_section_type_id,
        requirement_type: value.requirement_type as 'required' | 'optional' | 'excluded',
        position: value.position ? Number(value.position) : null,
      }))

    void updatePageRequirements({ id, sectionRequirements })
  }

  return (
    <DetailShell
      title=""
      backTo={pageRequirements ? `/page-strategy/${pageRequirements.page_strategy_id}` : undefined}
      backLabel="← Page strategy"
      data={pageRequirements}
      isLoading={isLoading}
      error={error}
    >
      <div className="space-y-4">
        <h2 className="text-lg font-semibold">Wymagania dotyczące sekcji</h2>

        {sectionsLoading && <p className="text-sm text-muted-foreground">Ładowanie…</p>}

        <div className="space-y-2">
          {sectionTypes?.map((section) => {
            const value = values[section.id] ?? {}

            return (
              <div
                key={section.id}
                className="grid grid-cols-1 items-start gap-3 bg-muted/25 p-3 sm:grid-cols-[1fr_10rem_6rem]"
              >
                <div>
                  <p className="text-sm font-medium">{section.name}</p>
                  <p className="text-xs text-muted-foreground">{section.description}</p>
                </div>

                <div>
                  <Label className="sr-only" htmlFor={`requirement-${section.id}`}>
                    Status sekcji {section.name}
                  </Label>
                  <Select
                    value={value.requirement_type}
                    onValueChange={(next) => next && setSectionValue(section.id, { requirement_type: next })}
                  >
                    <SelectTrigger id={`requirement-${section.id}`}>
                      <SelectValue placeholder="— (brak)" />
                    </SelectTrigger>
                    <SelectContent>
                      {REQUIREMENT_OPTIONS.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                          {option.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label className="sr-only" htmlFor={`position-${section.id}`}>
                    Pozycja sekcji {section.name}
                  </Label>
                  <Input
                    id={`position-${section.id}`}
                    type="number"
                    placeholder="pozycja"
                    value={value.position ?? ''}
                    disabled={!value.requirement_type}
                    onChange={(e) => setSectionValue(section.id, { position: e.target.value })}
                  />
                </div>
              </div>
            )
          })}
        </div>

        <Button onClick={handleSave} disabled={updateState.isLoading}>
          {updateState.isLoading ? 'Zapisywanie…' : 'Zapisz'}
        </Button>
      </div>
    </DetailShell>
  )
}
