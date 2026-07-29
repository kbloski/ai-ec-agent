import { api } from '@/store/api'

export interface ContentStatus {
  value: string
  label: string
}

export const contentStatusApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listContentStatuses: builder.query<ContentStatus[], void>({
      query: () => '/content-statuses',
    }),
  }),
})

export const { useListContentStatusesQuery } = contentStatusApi
