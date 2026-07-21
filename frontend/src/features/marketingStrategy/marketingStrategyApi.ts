import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const marketingStrategyApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listMarketingStrategyForBrandMarketing: builder.query<Entity[], number>({
      query: (brandMarketingId) => `/brand-marketing/${brandMarketingId}/marketing-strategy`,
      providesTags: (result, _err, brandMarketingId) => [
        ...(result ?? []).map((item) => itemTag('MarketingStrategy', item.id)),
        listTag('MarketingStrategy', brandMarketingId),
      ],
    }),
    getMarketingStrategy: builder.query<Entity, number>({
      query: (id) => `/marketing-strategy/${id}`,
      providesTags: (_result, _err, id) => [itemTag('MarketingStrategy', id)],
    }),
    /** ctx: the parent BrandMarketing entity (carries knowledge_id + id). */
    generateMarketingStrategy: builder.mutation<Entity, Entity>({
      query: (brandMarketing) =>
        `/knowledges/${brandMarketing.knowledge_id}/brand-marketing/${brandMarketing.id}/marketing-strategy/generate`,
      invalidatesTags: (_result, _err, brandMarketing) => [
        listTag('MarketingStrategy', brandMarketing.id),
      ],
    }),
    deleteMarketingStrategy: builder.mutation<void, { id: number; brandMarketingId: number }>({
      query: ({ id }) => `/marketing-strategy/${id}/delete`,
      invalidatesTags: (_result, _err, { id, brandMarketingId }) => [
        listTag('MarketingStrategy', brandMarketingId),
        itemTag('MarketingStrategy', id),
      ],
    }),
  }),
})

export const {
  useListMarketingStrategyForBrandMarketingQuery,
  useGetMarketingStrategyQuery,
  useGenerateMarketingStrategyMutation,
  useDeleteMarketingStrategyMutation,
} = marketingStrategyApi
