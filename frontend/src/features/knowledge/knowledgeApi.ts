import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const knowledgeApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listKnowledgeForOffer: builder.query<Entity[], number>({
      query: (offerId) => `/offers/${offerId}/knowledges`,
      providesTags: (result, _err, offerId) => [
        ...(result ?? []).map((item) => itemTag('Knowledge', item.id)),
        listTag('Knowledge', offerId),
      ],
    }),
    getKnowledge: builder.query<Entity, number>({
      query: (id) => `/knowledges/${id}`,
      providesTags: (_result, _err, id) => [itemTag('Knowledge', id)],
    }),
    updateKnowledge: builder.mutation<Entity, { id: number; fields: Record<string, unknown> }>({
      query: ({ id, fields }) => ({
        url: `/knowledges/${id}/update`,
        method: 'POST',
        body: { fields },
      }),
      invalidatesTags: (_result, _err, { id }) => [itemTag('Knowledge', id)],
    }),
    generateKnowledge: builder.mutation<Entity, { offerId: number }>({
      query: ({ offerId }) => `/offers/${offerId}/knowledges/generate`,
      invalidatesTags: (_result, _err, { offerId }) => [listTag('Knowledge', offerId)],
    }),
    deleteKnowledge: builder.mutation<void, { id: number; offerId: number }>({
      query: ({ id }) => `/knowledges/${id}/delete`,
      invalidatesTags: (_result, _err, { id, offerId }) => [
        listTag('Knowledge', offerId),
        itemTag('Knowledge', id),
      ],
    }),
    deleteKnowledgeInsight: builder.mutation<void, { id: number; knowledgeId: number }>({
      query: ({ id }) => `/knowledge-insights/${id}/delete`,
      invalidatesTags: (_result, _err, { knowledgeId }) => [itemTag('Knowledge', knowledgeId)],
    }),
    getKnowledgeInsight: builder.query<Entity, number>({
      query: (id) => `/knowledge-insights/${id}`,
      providesTags: (_result, _err, id) => [itemTag('KnowledgeInsight', id)],
    }),
    updateKnowledgeInsight: builder.mutation<
      Entity,
      { id: number; knowledgeId: number; content_status: string }
    >({
      query: ({ id, content_status }) => ({
        url: `/knowledge-insights/${id}/update`,
        method: 'POST',
        body: { content_status },
      }),
      invalidatesTags: (_result, _err, { id, knowledgeId }) => [
        itemTag('Knowledge', knowledgeId),
        itemTag('KnowledgeInsight', id),
      ],
    }),
  }),
})

export const {
  useListKnowledgeForOfferQuery,
  useGetKnowledgeQuery,
  useGenerateKnowledgeMutation,
  useDeleteKnowledgeMutation,
  useDeleteKnowledgeInsightMutation,
  useGetKnowledgeInsightQuery,
  useUpdateKnowledgeInsightMutation,
  useUpdateKnowledgeMutation,
} = knowledgeApi
