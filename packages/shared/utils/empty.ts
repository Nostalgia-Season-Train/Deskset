/* ==== 是否非空（非 null 非 undefined） ==== */
export function isEmpty(value: unknown): boolean {
  return value === null || value === undefined
}


/* ==== 是否 null ==== */
export function isNull(value: unknown): boolean {
  return value === null
}


/* ==== 是否 undefined ==== */
export function isUndefined(value: unknown): boolean {
  return value === undefined
}
