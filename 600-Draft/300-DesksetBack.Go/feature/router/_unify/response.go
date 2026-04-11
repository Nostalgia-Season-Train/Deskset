package _unify

type DesksetResponseJSON struct {
	Success bool   `json:"success"` // 操作是否成功：成功 true，失败 false
	Code    int    `json:"code"`    // 错误码：成功 0
	Message string `json:"message"` // 错误信息：成功 ""
	Result  any    `json:"result"`  // 结果
}
