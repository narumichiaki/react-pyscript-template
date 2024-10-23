import React, { JSX, StrictMode, useState } from "https://cdn.skypack.dev/react@17"
import ReactDOM from "https://cdn.skypack.dev/react-dom@17"

// バックエンドAPI
type CallApiFunction = (url: string, json_param: Record<string, any>) => Promise<Record<string, any>>
let callAPI: CallApiFunction

function App(): JSX.Element {
  const [count, setCount] = useState<number>(0)

  const handleClick = React.useCallback(() => {
    setCount((prevCount) => {
      const newCount = prevCount + 1
      callAPI("/log", { message: newCount }).catch(error => {
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