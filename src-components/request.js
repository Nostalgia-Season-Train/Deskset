import axios from 'axios'

// const server = await window.electron.server()  // 临时禁用

export const desksetReq = axios.create({
  baseURL: `http://127.0.0.1:6527`,
  headers: {
    Authorization: `Bearer`
  }
})
