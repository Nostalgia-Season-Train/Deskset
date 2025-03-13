import { readFile, BaseDirectory } from '@tauri-apps/plugin-fs'
import axios from 'axios'

export const getDesksetReq = async () => {
  // 读取配置
  const data = await readFile(`./config/deskset.json`, { baseDir: BaseDirectory.Resource })
  const config = JSON.parse(new TextDecoder().decode(data))

  // 获取 port
  const port = config['server-port']

  // 获取 token
  const formData = new FormData()
  formData.append('username', config.username)
  formData.append('password', config.password)

  const repLogin = await axios.post(`http://127.0.0.1:${port}/v0/access/login`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  const token = repLogin.data.access_token

  // 返回 desksetReq
  const desksetReq = axios.create({
    baseURL: `http://127.0.0.1:${port}`,
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  return desksetReq
}

export const getServerInfo = async () => {
  // 读取配置
  const data = await readFile(`./config/deskset.json`, { baseDir: BaseDirectory.Resource })
  const config = JSON.parse(new TextDecoder().decode(data))

  // 获取 port
  const port = config['server-port']

  // 获取 token
  const formData = new FormData()
  formData.append('username', config.username)
  formData.append('password', config.password)

  const repLogin = await axios.post(`http://127.0.0.1:${port}/v0/access/login`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  const token = repLogin.data.access_token

  // 返回 host、port 和 token
  return {
    host: '127.0.0.1',
    port: port,
    token: token
  }
}
