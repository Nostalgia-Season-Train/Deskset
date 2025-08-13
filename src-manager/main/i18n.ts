// @ts-ignore
import en from '@/i18n/en.json'

import { config } from '#manager/global'

const language = config.language

export const _t = (str: string) => {
  if (language == 'zh-cn')
    return str
  if (language == 'en')
    return en[str] ?? str
}
