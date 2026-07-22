import { api } from '@/store/api'

interface OutputPrompt {
  content: string
}

export const settingsApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getOutputPrompt: builder.query<OutputPrompt, void>({
      query: () => '/settings/output-prompt',
    }),
    saveOutputPrompt: builder.mutation<OutputPrompt, string>({
      query: (content) => ({
        url: '/settings/output-prompt',
        method: 'POST',
        body: { content },
      }),
    }),
  }),
})

export const { useGetOutputPromptQuery, useSaveOutputPromptMutation } = settingsApi
