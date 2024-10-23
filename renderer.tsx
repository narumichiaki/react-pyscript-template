import React, { JSX, StrictMode, useState } from "https://esm.sh/react@17.0"
import ReactDOM from "https://esm.sh/react-dom@17.0"
import { z } from "https://esm.sh/zod@3.23.8"

// バックエンドAPI
type CallApiFunction = (
  path: string,
  json_param: Record<string, any>,
  response_schema?: z.ZodType<any, any, any>
) => Promise<Record<string, any>>
let callAPI: CallApiFunction

// API Responce Validators (バグ予防のためにAPIから受け取る値をチェックする)
// for "/log"
const LogMessageSchema = z.object({
  message: z.string()
})


function App(): JSX.Element {
  const [count, setCount] = useState<number>(0)

  const handleClick = React.useCallback(() => {
    setCount((prevCount) => {
      const newCount = prevCount + 1
      // レスポンスのバリデーションあり版
      callAPI("/log", { message: newCount }, LogMessageSchema).then(response => {
        console.info(`Response: ${response.message}`)
      }).catch(error => {
        console.error("ログの記録に失敗しました。", {error})
      })
      // レスポンスのバリデーションなし版
      callAPI("/log_unsafe", { message: newCount }).then(response => {
        console.info(`Response: ${response.message}`)
      }).catch(error => {
        console.error("ログの記録に失敗しました。", {error})
      })
      return newCount
    })
  }, [])

  return (
    <div>
      <div>Count: {count}</div>
      <button onClick={handleClick}>Increment</button>
    </div>
  )
}


function render(call_api: CallApiFunction) {
  callAPI = call_api
  ReactDOM.render(
    <StrictMode>
      <App />
    </StrictMode>,
    document.getElementById('root') as HTMLElement
  )
}

// renderをwindowに登録(必須)
(window as any).render = render