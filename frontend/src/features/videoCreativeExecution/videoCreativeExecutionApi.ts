import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const videoCreativeExecutionApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listVideoCreativeExecutionForAdExecution: builder.query<Entity[], number>({
      query: (adExecutionId) => `/ad-execution/${adExecutionId}/video-creative-execution`,
      providesTags: (result, _err, adExecutionId) => [
        ...(result ?? []).map((item) => itemTag('VideoCreativeExecution', item.id)),
        listTag('VideoCreativeExecution', adExecutionId),
      ],
    }),
    getVideoCreativeExecution: builder.query<Entity, number>({
      query: (id) => `/video-creative-execution/${id}`,
      providesTags: (_result, _err, id) => [itemTag('VideoCreativeExecution', id)],
    }),
    generateVideoCreativeExecution: builder.mutation<
      Entity,
      { adExecutionId: number; duration_seconds?: number }
    >({
      query: ({ adExecutionId, ...params }) => ({
        url: `/ad-execution/${adExecutionId}/video-creative-execution/generate`,
        params,
      }),
      invalidatesTags: (_result, _err, { adExecutionId }) => [
        listTag('VideoCreativeExecution', adExecutionId),
      ],
    }),
    deleteVideoCreativeExecution: builder.mutation<void, { id: number; adExecutionId: number }>({
      query: ({ id }) => `/video-creative-execution/${id}/delete`,
      invalidatesTags: (_result, _err, { id, adExecutionId }) => [
        listTag('VideoCreativeExecution', adExecutionId),
        itemTag('VideoCreativeExecution', id),
      ],
    }),
  }),
})

export const {
  useListVideoCreativeExecutionForAdExecutionQuery,
  useGetVideoCreativeExecutionQuery,
  useGenerateVideoCreativeExecutionMutation,
  useDeleteVideoCreativeExecutionMutation,
} = videoCreativeExecutionApi
