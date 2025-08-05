import { reactive } from 'vue'

export const DEFAULT_SERVER_PORT = 6527
export const DEFAULT_USERNAME = 'username'
export const DEFAULT_PASSWORD = 'password'

export const config = reactive({
  isAutostart: false,
  closeBehavior: 'hide',

  server_port: DEFAULT_SERVER_PORT,
  username: DEFAULT_USERNAME,
  password: DEFAULT_PASSWORD
})
