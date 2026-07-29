import { api } from '@/store/api'

export interface CreativeAngle {
  id: string
  name: string
}

export const creativeAnglesApi = api.injectEndpoints({
  endpoints: (builder) => ({
    listCreativeAngles: builder.query<CreativeAngle[], void>({
      query: () => '/creative-angels',
    }),
  }),
})

export const { useListCreativeAnglesQuery } = creativeAnglesApi
