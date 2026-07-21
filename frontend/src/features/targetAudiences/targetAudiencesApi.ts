import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const targetAudiencesApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listTargetAudiencesForKnowledge: builder.query<Entity[], number>({
      query: (knowledgeId) => `/knowledges/${knowledgeId}/target-audiences`,
      providesTags: (result, _err, knowledgeId) => [
        ...(result ?? []).map((item) => itemTag('TargetAudience', item.id)),
        listTag('TargetAudience', knowledgeId),
      ],
    }),
    getTargetAudience: builder.query<Entity, number>({
      query: (id) => `/target-audiences/${id}`,
      providesTags: (_result, _err, id) => [itemTag('TargetAudience', id)],
    }),
    generateTargetAudiences: builder.mutation<Entity[], { knowledgeId: number }>({
      query: ({ knowledgeId }) => `/knowledges/${knowledgeId}/target-audiences/generate`,
      invalidatesTags: (_result, _err, { knowledgeId }) => [listTag('TargetAudience', knowledgeId)],
    }),
    deleteTargetAudience: builder.mutation<void, { id: number; knowledgeId: number }>({
      query: ({ id }) => `/target-audiences/${id}/delete`,
      invalidatesTags: (_result, _err, { id, knowledgeId }) => [
        listTag('TargetAudience', knowledgeId),
        itemTag('TargetAudience', id),
      ],
    }),
  }),
})

export const {
  useListTargetAudiencesForKnowledgeQuery,
  useGetTargetAudienceQuery,
  useGenerateTargetAudiencesMutation,
  useDeleteTargetAudienceMutation,
} = targetAudiencesApi
