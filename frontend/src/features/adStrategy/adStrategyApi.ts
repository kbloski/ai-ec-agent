import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const adStrategyApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listAdStrategyForMessageStrategy: builder.query<Entity[], number>({
      query: (messageStrategyId) => `/message-strategy/${messageStrategyId}/ad-strategy`,
      providesTags: (result, _err, messageStrategyId) => [
        ...(result ?? []).map((item) => itemTag('AdStrategy', item.id)),
        listTag('AdStrategy', messageStrategyId),
      ],
    }),
    getAdStrategy: builder.query<Entity, number>({
      query: (id) => `/ad-strategy/${id}`,
      providesTags: (_result, _err, id) => [itemTag('AdStrategy', id)],
    }),
    /** ctx: the parent MessageStrategy entity. */
    generateAdStrategy: builder.mutation<Entity, Entity>({
      query: (ms) =>
        `/knowledges/${ms.knowledge_id}/brand-marketing/${ms.brand_marketing_id}/marketing-strategy/${ms.marketing_strategy_id}/offer-strategy/${ms.offer_strategy_id}/message-strategy/${ms.id}/ad-strategy/generate`,
      invalidatesTags: (_result, _err, ms) => [listTag('AdStrategy', ms.id)],
    }),
  }),
})

export const {
  useListAdStrategyForMessageStrategyQuery,
  useGetAdStrategyQuery,
  useGenerateAdStrategyMutation,
} = adStrategyApi
