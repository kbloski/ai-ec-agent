import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const offerStrategyApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listOfferStrategyForMarketingStrategy: builder.query<Entity[], number>({
      query: (marketingStrategyId) => `/marketing-strategy/${marketingStrategyId}/offer-strategy`,
      providesTags: (result, _err, marketingStrategyId) => [
        ...(result ?? []).map((item) => itemTag('OfferStrategy', item.id)),
        listTag('OfferStrategy', marketingStrategyId),
      ],
    }),
    getOfferStrategy: builder.query<Entity, number>({
      query: (id) => `/offer-strategy/${id}`,
      providesTags: (_result, _err, id) => [itemTag('OfferStrategy', id)],
    }),
    /** ctx: the parent MarketingStrategy entity. */
    generateOfferStrategy: builder.mutation<Entity, Entity>({
      query: (ms) =>
        `/knowledges/${ms.knowledge_id}/brand-marketing/${ms.brand_marketing_id}/marketing-strategy/${ms.id}/offer-strategy/generate`,
      invalidatesTags: (_result, _err, ms) => [listTag('OfferStrategy', ms.id)],
    }),
    deleteOfferStrategy: builder.mutation<void, { id: number; marketingStrategyId: number }>({
      query: ({ id }) => `/offer-strategy/${id}/delete`,
      invalidatesTags: (_result, _err, { id, marketingStrategyId }) => [
        listTag('OfferStrategy', marketingStrategyId),
        itemTag('OfferStrategy', id),
      ],
    }),
  }),
})

export const {
  useListOfferStrategyForMarketingStrategyQuery,
  useGetOfferStrategyQuery,
  useGenerateOfferStrategyMutation,
  useDeleteOfferStrategyMutation,
} = offerStrategyApi
