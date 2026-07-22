export const TAG_TYPES = [
  'Offer',
  'Knowledge',
  'TargetAudience',
  'Analysis',
  'Checklist',
  'BrandMarketing',
  'MarketingStrategy',
  'OfferStrategy',
  'MessageStrategy',
  'AdStrategy',
  'CreativeStrategy',
  'AdExecution',
  'VideoCreativeExecution',
  'UgcCreative',
  'PageStrategy',
  'PageBlueprint',
  'PageContentPlan',
  'PageCopy',
] as const

export type Tag = (typeof TAG_TYPES)[number]

/** Tag for a parent-scoped list query — invalidated when a child is generated for that parent. */
export const listTag = (type: Tag, parentId: string | number) =>
  ({ type, id: `LIST_${parentId}` }) as const

/** Tag for a single entity's detail query. */
export const itemTag = (type: Tag, id: string | number) => ({ type, id }) as const
