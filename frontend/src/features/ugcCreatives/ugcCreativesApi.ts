import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const ugcCreativesApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listUgcCreativesForMessageStrategy: builder.query<Entity[], number>({
      query: (messageStrategyId) => `/message-strategy/${messageStrategyId}/ugc-creatives`,
      providesTags: (result, _err, messageStrategyId) => [
        ...(result ?? []).map((item) => itemTag('UgcCreative', item.id)),
        listTag('UgcCreative', messageStrategyId),
      ],
    }),
    getUgcCreative: builder.query<Entity, number>({
      query: (id) => `/ugc-creatives/${id}`,
      providesTags: (_result, _err, id) => [itemTag('UgcCreative', id)],
    }),
    /** ctx: the parent MessageStrategy entity. */
    generateUgcCreatives: builder.mutation<Entity[], Entity>({
      query: (ms) =>
        `/knowledges/${ms.knowledge_id}/brand-marketing/${ms.brand_marketing_id}/marketing-strategy/${ms.marketing_strategy_id}/offer-strategy/${ms.offer_strategy_id}/message-strategy/${ms.id}/ugc-creatives/generate`,
      invalidatesTags: (_result, _err, ms) => [listTag('UgcCreative', ms.id)],
    }),
  }),
})

export const {
  useListUgcCreativesForMessageStrategyQuery,
  useGetUgcCreativeQuery,
  useGenerateUgcCreativesMutation,
} = ugcCreativesApi
