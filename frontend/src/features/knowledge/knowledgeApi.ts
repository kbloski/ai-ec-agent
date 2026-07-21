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
  }),
})

export const {
  useListKnowledgeForOfferQuery,
  useGetKnowledgeQuery,
  useGenerateKnowledgeMutation,
  useDeleteKnowledgeMutation,
  useDeleteKnowledgeInsightMutation,
} = knowledgeApi
