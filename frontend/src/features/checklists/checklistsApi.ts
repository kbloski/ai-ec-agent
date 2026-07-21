import { api } from '@/store/api'
import { listTag, itemTag } from '@/lib/tags'
import type { Entity } from '@/types'

export const checklistsApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listChecklistsForAnalysis: builder.query<Entity[], number>({
      query: (analysisId) => `/analysis/${analysisId}/checklists`,
      providesTags: (result, _err, analysisId) => [
        ...(result ?? []).map((item) => itemTag('Checklist', item.id)),
        listTag('Checklist', analysisId),
      ],
    }),
    getChecklist: builder.query<Entity, number>({
      query: (id) => `/checklists/${id}`,
      providesTags: (_result, _err, id) => [itemTag('Checklist', id)],
    }),
    createChecklist: builder.mutation<Entity, { knowledgeId: number; analysisId: number }>({
      query: ({ knowledgeId, analysisId }) =>
        `/knowledges/${knowledgeId}/analysis/${analysisId}/checklists/create`,
      invalidatesTags: (_result, _err, { analysisId }) => [listTag('Checklist', analysisId)],
    }),
    generateChecklist: builder.mutation<
      Entity,
      { knowledgeId: number; analysisId: number; checklistId: number }
    >({
      query: ({ knowledgeId, analysisId, checklistId }) =>
        `/knowledges/${knowledgeId}/analysis/${analysisId}/checklists/${checklistId}/generate`,
      invalidatesTags: (_result, _err, { checklistId }) => [itemTag('Checklist', checklistId)],
    }),
    deleteChecklistItem: builder.mutation<void, { id: number; checklistId: number }>({
      query: ({ id }) => `/checklist-items/${id}/delete`,
      invalidatesTags: (_result, _err, { checklistId }) => [itemTag('Checklist', checklistId)],
    }),
    deleteChecklist: builder.mutation<void, { id: number; analysisId: number }>({
      query: ({ id }) => `/checklists/${id}/delete`,
      invalidatesTags: (_result, _err, { id, analysisId }) => [
        listTag('Checklist', analysisId),
        itemTag('Checklist', id),
      ],
    }),
  }),
})

export const {
  useListChecklistsForAnalysisQuery,
  useGetChecklistQuery,
  useCreateChecklistMutation,
  useGenerateChecklistMutation,
  useDeleteChecklistItemMutation,
  useDeleteChecklistMutation,
} = checklistsApi
