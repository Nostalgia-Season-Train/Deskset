import axios from 'axios'

const server = await window.electron.server()

export const desksetReq = axios.create({
  baseURL: `http://127.0.0.1:${server.port}`,
  headers: {
    Authorization: `Bearer ${server.token}`
  }
})
