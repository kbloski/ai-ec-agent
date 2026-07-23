import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const creativeExecutionApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listCreativeExecutionForAdExecution: builder.query<Entity[], number>({
      query: (adExecutionId) => `/ad-execution/${adExecutionId}/creative-execution`,
      providesTags: (result, _err, adExecutionId) => [
        ...(result ?? []).map((item) => itemTag('CreativeExecution', item.id)),
        listTag('CreativeExecution', adExecutionId),
      ],
    }),
    getCreativeExecution: builder.query<Entity, number>({
      query: (id) => `/creative-execution/${id}`,
      providesTags: (_result, _err, id) => [itemTag('CreativeExecution', id)],
    }),
    generateCreativeExecution: builder.mutation<
      Entity,
      { adExecutionId: number; duration_seconds?: number }
    >({
      query: ({ adExecutionId, ...params }) => ({
        url: `/ad-execution/${adExecutionId}/creative-execution/generate`,
        params,
      }),
      invalidatesTags: (_result, _err, { adExecutionId }) => [
        listTag('CreativeExecution', adExecutionId),
      ],
    }),
    deleteCreativeExecution: builder.mutation<void, { id: number; adExecutionId: number }>({
      query: ({ id }) => `/creative-execution/${id}/delete`,
      invalidatesTags: (_result, _err, { id, adExecutionId }) => [
        listTag('CreativeExecution', adExecutionId),
        itemTag('CreativeExecution', id),
      ],
    }),
  }),
})

export const {
  useListCreativeExecutionForAdExecutionQuery,
  useGetCreativeExecutionQuery,
  useGenerateCreativeExecutionMutation,
  useDeleteCreativeExecutionMutation,
} = creativeExecutionApi
