import { api } from '@/store/api'

export interface Platform {
  id: string
  name: string
  aspect_ratio: string
  description: string
  rules: string[]
}

export const platformsApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listPlatforms: builder.query<Platform[], void>({
      query: () => '/platforms',
    }),
  }),
})

export const { useListPlatformsQuery } = platformsApi
