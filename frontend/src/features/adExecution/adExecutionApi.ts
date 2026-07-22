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
        url: `/creative-strategy/${cs.id}/ad-execution/generate`,
        params,
      }),
      invalidatesTags: (_result, _err, { creativeStrategy }) => [
        listTag('AdExecution', creativeStrategy.id),
      ],
    }),
    deleteAdExecution: builder.mutation<void, { id: number; creativeStrategyId: number }>({
      query: ({ id }) => `/ad-execution/${id}/delete`,
      invalidatesTags: (_result, _err, { id, creativeStrategyId }) => [
        listTag('AdExecution', creativeStrategyId),
        itemTag('AdExecution', id),
      ],
    }),
  }),
})

export const {
  useListAdExecutionForCreativeStrategyQuery,
  useGetAdExecutionQuery,
  useGenerateAdExecutionMutation,
  useDeleteAdExecutionMutation,
} = adExecutionApi
