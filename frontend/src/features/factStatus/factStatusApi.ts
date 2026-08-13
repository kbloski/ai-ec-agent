import { api } from '@/store/api'

export interface FactStatus {
  value: string
  label: string
}

export const factStatusApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listFactStatuses: builder.query<FactStatus[], void>({
      query: () => '/fact-statuses',
    }),
  }),
})

export const { useListFactStatusesQuery } = factStatusApi
