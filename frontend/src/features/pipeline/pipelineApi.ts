import { api } from '@/store/api'

export interface PipelinePathStage {
  stage: string
  id: number
  data: Record<string, unknown>
  llm_context: string | null
}

export interface PipelinePathResponse {
  requested: { entity_type: string; entity_id: number }
  path: PipelinePathStage[]
}

export const pipelineApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getPipelinePath: builder.mutation<PipelinePathResponse, { entity_type: string; entity_id: number }>({
      query: (body) => ({
        url: '/pipeline/path',
        method: 'POST',
        body,
      }),
    }),
  }),
})

export const { useGetPipelinePathMutation } = pipelineApi
