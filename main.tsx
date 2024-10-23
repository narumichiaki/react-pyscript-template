export {}

// Reactの中からPyScriptの関数を呼べるように、Python Interpreter (Pyodide)を取りだす
import { hooks } from "https://pyscript.net/releases/2024.10.1/core.js"
hooks.main.onReady.add((wrap, element) => {
    (window as any).pyInterpreter = wrap.interpreter
})

// api_endpointのwrapper - オブジェクトをstringifyして送り、返ってきたJSON stringをオブジェクトに展開して返す
function _callAPI(path: string, json_param: Record<string, any>): Record<string, any> {
    try {
        const json_string = JSON.stringify(json_param)
        const result = (window as any).api_endpoint(path, json_string)
        return JSON.parse(result)
    } catch (error) {
        console.error('API呼び出し中にエラーが発生しました:', error)
        throw error
    }
}

// フロントエンドとバックエンドのロードが完了するまで待つ (最大10秒)
function waitForLoaded(timeout: number = 10000): Promise<void> {
    return new Promise((resolve, reject) => {
        const startTime = Date.now()
        const intervalId = setInterval(() => {
            if (typeof (window as any).api_endpoint === 'function' && typeof (window as any).render === 'function') {
                clearInterval(intervalId)
                resolve()
            }
            if (Date.now() - startTime > timeout) {
                clearInterval(intervalId)
                if (typeof (window as any).render !== 'function') {
                    reject(new Error("フロントエンドのロードに失敗しました。"))
                }
                if (typeof (window as any).api_endpoint !== 'function') {
                    reject(new Error("バックエンドのロードに失敗しました。"))
                }
            }
        }, 100)
    })
}

// 実行
await waitForLoaded().then(() => {
    (window as any).render(_callAPI)
}).catch(error => {
    throw error
})
