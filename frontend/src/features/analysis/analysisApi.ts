import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const analysisApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listAnalysisForKnowledge: builder.query<Entity[], number>({
      query: (knowledgeId) => `/knowledges/${knowledgeId}/analysis`,
      providesTags: (result, _err, knowledgeId) => [
        ...(result ?? []).map((item) => itemTag('Analysis', item.id)),
        listTag('Analysis', knowledgeId),
      ],
    }),
    getAnalysis: builder.query<Entity, number>({
      query: (id) => `/analysis/${id}`,
      providesTags: (_result, _err, id) => [itemTag('Analysis', id)],
    }),
    createAnalysis: builder.mutation<Entity, { knowledgeId: number }>({
      query: ({ knowledgeId }) => `/knowledges/${knowledgeId}/analysis/create`,
      invalidatesTags: (_result, _err, { knowledgeId }) => [listTag('Analysis', knowledgeId)],
    }),
    generateAnalysisAnswers: builder.mutation<Entity, { knowledgeId: number; analysisId: number }>({
      query: ({ knowledgeId, analysisId }) =>
        `/knowledges/${knowledgeId}/analysis/${analysisId}/answers/generate`,
      invalidatesTags: (_result, _err, { analysisId }) => [itemTag('Analysis', analysisId)],
    }),
    deleteAnalysis: builder.mutation<void, { id: number; knowledgeId: number }>({
      query: ({ id }) => `/analysis/${id}/delete`,
      invalidatesTags: (_result, _err, { id, knowledgeId }) => [
        listTag('Analysis', knowledgeId),
        itemTag('Analysis', id),
      ],
    }),
    deleteAnalysisQuestion: builder.mutation<void, { id: number; analysisId: number }>({
      query: ({ id }) => `/analysis-questions/${id}/delete`,
      invalidatesTags: (_result, _err, { analysisId }) => [itemTag('Analysis', analysisId)],
    }),
  }),
})

export const {
  useListAnalysisForKnowledgeQuery,
  useGetAnalysisQuery,
  useCreateAnalysisMutation,
  useGenerateAnalysisAnswersMutation,
  useDeleteAnalysisMutation,
  useDeleteAnalysisQuestionMutation,
} = analysisApi
