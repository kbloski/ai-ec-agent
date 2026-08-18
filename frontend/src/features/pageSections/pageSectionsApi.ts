import { api } from '@/store/api'

export interface PageSectionType {
  id: string
  name: string
  description: string
}

export const pageSectionsApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listPageSections: builder.query<PageSectionType[], void>({
      query: () => '/page-sections',
    }),
  }),
})

export const { useListPageSectionsQuery } = pageSectionsApi
