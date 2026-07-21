/** Generic shape of any backend DTO: an id plus arbitrary fields (including ancestor *_id fields). */
export interface Entity {
  id: number
  [key: string]: unknown
}
