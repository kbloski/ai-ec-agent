import { isRejectedWithValue, type Middleware } from '@reduxjs/toolkit'
import { toast } from 'sonner'

type UnknownRecord = Record<string, unknown>

function asRecord(value: unknown): UnknownRecord | undefined {
  return typeof value === 'object' && value !== null ? (value as UnknownRecord) : undefined
}

function stringifyDetail(value: unknown): string | undefined {
  if (typeof value === 'string') return value || undefined
  if (typeof value === 'number' || typeof value === 'boolean') return String(value)

  if (Array.isArray(value)) {
    const messages = value.map((item) => {
      const detail = asRecord(item)
      if (!detail) return stringifyDetail(item)

      const location = Array.isArray(detail.loc)
        ? detail.loc.filter((part) => part !== 'body').join('.')
        : undefined
      const message = stringifyDetail(detail.msg) ?? JSON.stringify(detail)
      const type = stringifyDetail(detail.type)

      return [location, message, type ? `(${type})` : undefined].filter(Boolean).join(': ')
    })

    return messages.filter(Boolean).join('\n') || undefined
  }

  if (value && typeof value === 'object') {
    return JSON.stringify(value, null, 2)
  }

  return undefined
}

function getApiErrorMessage(payload: unknown): string {
  const error = asRecord(payload)
  if (!error) return 'Nie udało się wykonać zapytania.'

  if (error.status === 'FETCH_ERROR') {
    const detail = stringifyDetail(error.error)
    return [
      'Nie można połączyć się z API.',
      detail,
    ].filter(Boolean).join('\n')
  }

  if (error.status === 'TIMEOUT_ERROR') {
    const detail = stringifyDetail(error.error)
    return ['API nie odpowiedziało w wymaganym czasie.', detail].filter(Boolean).join('\n')
  }

  const data = asRecord(error.data)
  const responseDetail =
    stringifyDetail(data?.detail) ??
    stringifyDetail(data?.message) ??
    stringifyDetail(data?.error) ??
    stringifyDetail(error.data) ??
    stringifyDetail(error.error)
  const status =
    typeof error.status === 'number'
      ? `HTTP ${error.status}`
      : error.status === 'PARSING_ERROR' && typeof error.originalStatus === 'number'
        ? `HTTP ${error.originalStatus} · błąd odpowiedzi JSON`
        : stringifyDetail(error.status)

  return [status, responseDetail ?? 'Nie udało się wykonać zapytania.'].filter(Boolean).join('\n')
}

/** Displays one global notification for every failed RTK Query request or mutation. */
export const apiErrorMiddleware: Middleware = () => (next) => (action) => {
  if (isRejectedWithValue(action)) {
    const meta = asRecord(action.meta)
    const argument = asRecord(meta?.arg)

    if (argument?.type === 'query' || argument?.type === 'mutation') {
      const endpointName =
        typeof argument.endpointName === 'string' ? argument.endpointName : 'nieznana operacja'

      toast.error(`Błąd API: ${endpointName}`, {
        description: getApiErrorMessage(action.payload),
        duration: 10_000,
      })
    }
  }

  return next(action)
}
