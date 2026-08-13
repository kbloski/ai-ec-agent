import { api } from '@/store/api'

export interface ReviewStatus {
  value: string
  label: string
}

export const reviewStatusApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listReviewStatuses: builder.query<ReviewStatus[], void>({
      query: () => '/review-statuses',
    }),
  }),
})

export const { useListReviewStatusesQuery } = reviewStatusApi
