import { api } from '@/store/api'

export interface AdFramework {
  id: string
  name: string
}

export const adFrameworksApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listAdFrameworks: builder.query<AdFramework[], void>({
      query: () => '/ad-frameworks',
    }),
  }),
})

export const { useListAdFrameworksQuery } = adFrameworksApi
