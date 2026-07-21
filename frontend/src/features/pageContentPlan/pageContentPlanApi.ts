import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

interface GenerateArgs {
  /** The owning MessageStrategy entity — its `.id` is the `message_strategy_id`. */
  chain: Entity
  pageStrategyId: number
  pageBlueprintId: number
}

export const pageContentPlanApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listPageContentPlanForPageBlueprint: builder.query<Entity[], number>({
      query: (pageBlueprintId) => `/page-blueprint/${pageBlueprintId}/page-content-plan`,
      providesTags: (result, _err, pageBlueprintId) => [
        ...(result ?? []).map((item) => itemTag('PageContentPlan', item.id)),
        listTag('PageContentPlan', pageBlueprintId),
      ],
    }),
    getPageContentPlan: builder.query<Entity, number>({
      query: (id) => `/page-content-plan/${id}`,
      providesTags: (_result, _err, id) => [itemTag('PageContentPlan', id)],
    }),
    generatePageContentPlan: builder.mutation<Entity, GenerateArgs>({
      query: ({ chain, pageStrategyId, pageBlueprintId }) =>
        `/knowledges/${chain.knowledge_id}/brand-marketing/${chain.brand_marketing_id}/marketing-strategy/${chain.marketing_strategy_id}/offer-strategy/${chain.offer_strategy_id}/message-strategy/${chain.id}/page-strategy/${pageStrategyId}/page-blueprint/${pageBlueprintId}/page-content-plan/generate`,
      invalidatesTags: (_result, _err, { pageBlueprintId }) => [
        listTag('PageContentPlan', pageBlueprintId),
      ],
    }),
    deletePageContentPlan: builder.mutation<void, { id: number; pageBlueprintId: number }>({
      query: ({ id }) => `/page-content-plan/${id}/delete`,
      invalidatesTags: (_result, _err, { id, pageBlueprintId }) => [
        listTag('PageContentPlan', pageBlueprintId),
        itemTag('PageContentPlan', id),
      ],
    }),
  }),
})

export const {
  useListPageContentPlanForPageBlueprintQuery,
  useGetPageContentPlanQuery,
  useGeneratePageContentPlanMutation,
  useDeletePageContentPlanMutation,
} = pageContentPlanApi
