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
  }),
})

export const {
  useListKnowledgeForOfferQuery,
  useGetKnowledgeQuery,
  useGenerateKnowledgeMutation,
} = knowledgeApi
