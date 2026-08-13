import { api } from '@/store/api'

export interface AdFrameworkStep {
  step: number
  name: string
  purpose: string
}

export interface AdFramework {
  id: string
  name: string
  format?: string
  goal?: string
  description?: string
  rules?: string[]
  structure?: AdFrameworkStep[]
}

export const adFrameworksApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listAdFrameworks: builder.query<AdFramework[], void>({
      query: () => '/ad-frameworks',
    }),
  }),
})

export const { useListAdFrameworksQuery } = adFrameworksApi
