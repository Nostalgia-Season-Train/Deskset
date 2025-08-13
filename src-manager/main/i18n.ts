// @ts-ignore
import en from '@/i18n/en.json'

const language = 'zh-cn'

export const _t = (str: string) => {
  if (language == 'zh-cn')
    return str
  if (language == 'en')
    return en[str] ?? str
}
