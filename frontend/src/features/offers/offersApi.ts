import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

interface OffersResponse {
  items: Entity[]
  page: number
  page_size: number
  total_items: number
}

interface CreateOfferArgs {
  name: string
  buying_price: number
  selling_price?: number
  details?: string
}

export const offersApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listOffers: builder.query<OffersResponse, { page?: number } | void>({
      query: (params) => ({
        url: '/offers',
        params: { page: params?.page ?? 1 },
      }),
      providesTags: (result) => [
        ...(result?.items ?? []).map((item) => itemTag('Offer', item.id)),
        listTag('Offer', 'root'),
      ],
    }),
    getOffer: builder.query<Entity, number>({
      query: (id) => `/offers/${id}`,
      providesTags: (_result, _err, id) => [itemTag('Offer', id)],
    }),
    createOffer: builder.mutation<Entity, CreateOfferArgs>({
      query: (params) => ({ url: '/offers/create', params }),
      invalidatesTags: [listTag('Offer', 'root')],
    }),
    deleteOffer: builder.mutation<void, number>({
      query: (id) => `/offers/${id}/delete`,
      invalidatesTags: (_result, _err, id) => [listTag('Offer', 'root'), itemTag('Offer', id)],
    }),
    deleteOfferItem: builder.mutation<void, { id: number; offerId: number }>({
      query: ({ id }) => `/offer-items/${id}/delete`,
      invalidatesTags: (_result, _err, { offerId }) => [itemTag('Offer', offerId)],
    }),
    deleteOfferInsight: builder.mutation<void, { id: number; offerId: number }>({
      query: ({ id }) => `/offer-insights/${id}/delete`,
      invalidatesTags: (_result, _err, { offerId }) => [itemTag('Offer', offerId)],
    }),
    getOfferInsight: builder.query<Entity, number>({
      query: (id) => `/offer-insights/${id}`,
      providesTags: (_result, _err, id) => [itemTag('OfferInsight', id)],
    }),
    updateOfferInsight: builder.mutation<Entity, { id: number; offerId: number; content_status: string }>({
      query: ({ id, content_status }) => ({
        url: `/offer-insights/${id}/update`,
        method: 'POST',
        body: { content_status },
      }),
      invalidatesTags: (_result, _err, { id, offerId }) => [
        itemTag('Offer', offerId),
        itemTag('OfferInsight', id),
      ],
    }),
    generateOfferSuggestions: builder.mutation<Entity, number>({
      query: (id) => `/offers/${id}/suggestions`,
      invalidatesTags: (_result, _err, id) => [itemTag('Offer', id)],
    }),
  }),
})

export const {
  useListOffersQuery,
  useGetOfferQuery,
  useCreateOfferMutation,
  useDeleteOfferMutation,
  useDeleteOfferItemMutation,
  useDeleteOfferInsightMutation,
  useGenerateOfferSuggestionsMutation,
  useGetOfferInsightQuery,
  useUpdateOfferInsightMutation,
} = offersApi
