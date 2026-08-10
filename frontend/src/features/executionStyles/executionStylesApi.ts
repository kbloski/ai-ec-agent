import { api } from '@/store/api'

export interface ExecutionStyle {
  id: string
  name: string
  description: string
  rules: string[]
}

export const executionStylesApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listExecutionStyles: builder.query<ExecutionStyle[], void>({
      query: () => '/execution-styles',
    }),
  }),
})

export const { useListExecutionStylesQuery } = executionStylesApi
