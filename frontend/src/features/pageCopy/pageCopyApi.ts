import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

interface GenerateArgs {
  /** The owning MessageStrategy entity — its `.id` is the `message_strategy_id`. */
  chain: Entity
  pageStrategyId: number
  pageBlueprintId: number
  pageContentPlanId: number
}

export const pageCopyApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listPageCopyForPageContentPlan: builder.query<Entity[], number>({
      query: (pageContentPlanId) => `/page-content-plan/${pageContentPlanId}/page-copy`,
      providesTags: (result, _err, pageContentPlanId) => [
        ...(result ?? []).map((item) => itemTag('PageCopy', item.id)),
        listTag('PageCopy', pageContentPlanId),
      ],
    }),
    getPageCopy: builder.query<Entity, number>({
      query: (id) => `/page-copy/${id}`,
      providesTags: (_result, _err, id) => [itemTag('PageCopy', id)],
    }),
    generatePageCopy: builder.mutation<Entity, GenerateArgs>({
      query: ({ chain, pageStrategyId, pageBlueprintId, pageContentPlanId }) =>
        `/knowledges/${chain.knowledge_id}/brand-marketing/${chain.brand_marketing_id}/marketing-strategy/${chain.marketing_strategy_id}/offer-strategy/${chain.offer_strategy_id}/message-strategy/${chain.id}/page-strategy/${pageStrategyId}/page-blueprint/${pageBlueprintId}/page-content-plan/${pageContentPlanId}/page-copy/generate`,
      invalidatesTags: (_result, _err, { pageContentPlanId }) => [
        listTag('PageCopy', pageContentPlanId),
      ],
    }),
    deletePageCopy: builder.mutation<void, { id: number; pageContentPlanId: number }>({
      query: ({ id }) => `/page-copy/${id}/delete`,
      invalidatesTags: (_result, _err, { id, pageContentPlanId }) => [
        listTag('PageCopy', pageContentPlanId),
        itemTag('PageCopy', id),
      ],
    }),
  }),
})

export const {
  useListPageCopyForPageContentPlanQuery,
  useGetPageCopyQuery,
  useGeneratePageCopyMutation,
  useDeletePageCopyMutation,
} = pageCopyApi
