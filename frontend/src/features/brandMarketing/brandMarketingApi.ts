import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const brandMarketingApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listBrandMarketingForKnowledge: builder.query<Entity[], number>({
      query: (knowledgeId) => `/knowledges/${knowledgeId}/brand-marketing`,
      providesTags: (result, _err, knowledgeId) => [
        ...(result ?? []).map((item) => itemTag('BrandMarketing', item.id)),
        listTag('BrandMarketing', knowledgeId),
      ],
    }),
    getBrandMarketing: builder.query<Entity, number>({
      query: (id) => `/brand-marketing/${id}`,
      providesTags: (_result, _err, id) => [itemTag('BrandMarketing', id)],
    }),
    generateBrandMarketing: builder.mutation<Entity, { knowledgeId: number }>({
      query: ({ knowledgeId }) => `/knowledges/${knowledgeId}/brand-marketing/generate`,
      invalidatesTags: (_result, _err, { knowledgeId }) => [listTag('BrandMarketing', knowledgeId)],
    }),
  }),
})

export const {
  useListBrandMarketingForKnowledgeQuery,
  useGetBrandMarketingQuery,
  useGenerateBrandMarketingMutation,
} = brandMarketingApi
