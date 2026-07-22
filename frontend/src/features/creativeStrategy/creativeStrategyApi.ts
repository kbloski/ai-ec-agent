import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const creativeStrategyApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listCreativeStrategyForAdStrategy: builder.query<Entity[], number>({
      query: (adStrategyId) => `/ad-strategy/${adStrategyId}/creative-strategy`,
      providesTags: (result, _err, adStrategyId) => [
        ...(result ?? []).map((item) => itemTag('CreativeStrategy', item.id)),
        listTag('CreativeStrategy', adStrategyId),
      ],
    }),
    getCreativeStrategy: builder.query<Entity, number>({
      query: (id) => `/creative-strategy/${id}`,
      providesTags: (_result, _err, id) => [itemTag('CreativeStrategy', id)],
    }),
    /** ctx: the parent AdStrategy entity. */
    generateCreativeStrategy: builder.mutation<Entity, Entity>({
      query: (as) => `/ad-strategy/${as.id}/creative-strategy/generate`,
      invalidatesTags: (_result, _err, as) => [listTag('CreativeStrategy', as.id)],
    }),
    deleteCreativeStrategy: builder.mutation<void, { id: number; adStrategyId: number }>({
      query: ({ id }) => `/creative-strategy/${id}/delete`,
      invalidatesTags: (_result, _err, { id, adStrategyId }) => [
        listTag('CreativeStrategy', adStrategyId),
        itemTag('CreativeStrategy', id),
      ],
    }),
  }),
})

export const {
  useListCreativeStrategyForAdStrategyQuery,
  useGetCreativeStrategyQuery,
  useGenerateCreativeStrategyMutation,
  useDeleteCreativeStrategyMutation,
} = creativeStrategyApi
