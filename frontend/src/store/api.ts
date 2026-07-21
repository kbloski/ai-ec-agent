import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { TAG_TYPES } from '@/lib/tags'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8002'

/**
 * Base RTK Query API slice. Feature modules extend this via
 * `api.injectEndpoints({ ... })` instead of creating separate `createApi`
 * instances, so every endpoint shares one cache/middleware.
 */
export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: API_URL }),
  tagTypes: TAG_TYPES,
  endpoints: () => ({}),
})
