import { api } from '@/store/api'

export interface Offer {
  id: number
  name: string
  [key: string]: unknown
}

interface OffersResponse {
  items: Offer[]
}

/**
 * Example feature slice showing the convention: extend the shared `api`
 * via `injectEndpoints` rather than creating a new `createApi` instance.
 * Mirrors the backend's `GET /offers?page=` (see APPLICATION_FLOW.md).
 */
export const offersApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getOffers: builder.query<OffersResponse, { page?: number } | void>({
      query: (params) => ({
        url: '/offers',
        params: { page: params?.page ?? 1 },
      }),
    }),
  }),
})

export const { useGetOffersQuery } = offersApi
