import { Command, Child } from '@tauri-apps/plugin-shell'

let server: Child | null = null

export const spawnServer = async (): Promise<{
  url: string,
  token: string
}> => {
  const command = Command.sidecar('DesksetBack')

  server = await command.spawn()

  return await new Promise((resolve, reject) => {
    command.stdout.once('data', data => {
      resolve(JSON.parse(data))
    })
    command.once('close', data => {
      reject(data.code)  // 报错退出码
    })
  })
}

export const killServe = async () => {
  if (server == null)
    return
  await server.kill()
}
