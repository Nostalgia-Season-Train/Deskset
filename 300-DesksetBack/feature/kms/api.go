package kms

var rpcClient *RpcClient = nil

func SetOnline(RpcClient *RpcClient) {
	rpcClient = RpcClient
}

func SetOffline() {
	rpcClient = nil
}

func GetActiveFile() (any, error) {
	if rpcClient == nil {
		return nil, nil
	}
	return rpcClient.CallRemoteProcedure("get_active_file", []any{})
}
