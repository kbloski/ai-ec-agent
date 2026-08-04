import { configureStore } from '@reduxjs/toolkit'
import { api } from './api'
import { apiErrorMiddleware } from './apiErrorMiddleware'

export const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(apiErrorMiddleware, api.middleware),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
