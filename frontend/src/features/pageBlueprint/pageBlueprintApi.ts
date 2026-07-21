import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

interface GenerateArgs {
  /** The owning MessageStrategy entity — its `.id` is the `message_strategy_id`. */
  chain: Entity
  pageStrategyId: number
}

export const pageBlueprintApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listPageBlueprintForPageStrategy: builder.query<Entity[], number>({
      query: (pageStrategyId) => `/page-strategy/${pageStrategyId}/page-blueprint`,
      providesTags: (result, _err, pageStrategyId) => [
        ...(result ?? []).map((item) => itemTag('PageBlueprint', item.id)),
        listTag('PageBlueprint', pageStrategyId),
      ],
    }),
    getPageBlueprint: builder.query<Entity, number>({
      query: (id) => `/page-blueprint/${id}`,
      providesTags: (_result, _err, id) => [itemTag('PageBlueprint', id)],
    }),
    generatePageBlueprint: builder.mutation<Entity, GenerateArgs>({
      query: ({ chain, pageStrategyId }) =>
        `/knowledges/${chain.knowledge_id}/brand-marketing/${chain.brand_marketing_id}/marketing-strategy/${chain.marketing_strategy_id}/offer-strategy/${chain.offer_strategy_id}/message-strategy/${chain.id}/page-strategy/${pageStrategyId}/page-blueprint/generate`,
      invalidatesTags: (_result, _err, { pageStrategyId }) => [listTag('PageBlueprint', pageStrategyId)],
    }),
    deletePageBlueprint: builder.mutation<void, { id: number; pageStrategyId: number }>({
      query: ({ id }) => `/page-blueprint/${id}/delete`,
      invalidatesTags: (_result, _err, { id, pageStrategyId }) => [
        listTag('PageBlueprint', pageStrategyId),
        itemTag('PageBlueprint', id),
      ],
    }),
  }),
})

export const {
  useListPageBlueprintForPageStrategyQuery,
  useGetPageBlueprintQuery,
  useGeneratePageBlueprintMutation,
  useDeletePageBlueprintMutation,
} = pageBlueprintApi
