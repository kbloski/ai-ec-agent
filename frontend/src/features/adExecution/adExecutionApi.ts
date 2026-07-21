import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

interface GenerateAdExecutionArgs {
  creativeStrategy: Entity
  video_duration_seconds?: number
  platform?: string
  format?: string
}

export const adExecutionApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listAdExecutionForCreativeStrategy: builder.query<Entity[], number>({
      query: (creativeStrategyId) => `/creative-strategy/${creativeStrategyId}/ad-execution`,
      providesTags: (result, _err, creativeStrategyId) => [
        ...(result ?? []).map((item) => itemTag('AdExecution', item.id)),
        listTag('AdExecution', creativeStrategyId),
      ],
    }),
    getAdExecution: builder.query<Entity, number>({
      query: (id) => `/ad-execution/${id}`,
      providesTags: (_result, _err, id) => [itemTag('AdExecution', id)],
    }),
    generateAdExecution: builder.mutation<Entity, GenerateAdExecutionArgs>({
      query: ({ creativeStrategy: cs, ...params }) => ({
        url: `/knowledges/${cs.knowledge_id}/brand-marketing/${cs.brand_marketing_id}/marketing-strategy/${cs.marketing_strategy_id}/offer-strategy/${cs.offer_strategy_id}/message-strategy/${cs.message_strategy_id}/ad-strategy/${cs.ad_strategy_id}/creative-strategy/${cs.id}/ad-execution/generate`,
        params,
      }),
      invalidatesTags: (_result, _err, { creativeStrategy }) => [
        listTag('AdExecution', creativeStrategy.id),
      ],
    }),
  }),
})

export const {
  useListAdExecutionForCreativeStrategyQuery,
  useGetAdExecutionQuery,
  useGenerateAdExecutionMutation,
} = adExecutionApi
