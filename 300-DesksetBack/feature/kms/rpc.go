package kms

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"errors"
	"sync"

	"github.com/gofiber/contrib/v3/websocket"
)

type DesksetError struct {
	Message string `json:"message"`
}

func (e *DesksetError) Error() string {
	return e.Message
}

type RpcRequest struct {
	ID        string `json:"id"`
	Procedure string `json:"procedure"`
	Args      []any  `json:"args"`
}

type RpcResponse struct {
	ID      string    `json:"id"`
	Payload any       `json:"payload,omitempty"`
	Error   *RpcError `json:"error,omitempty"`
}

type RpcError struct {
	Message        string `json:"message"`
	IsDesksetError bool   `json:"is_deskset_error,omitempty"`
}

type RpcClient struct {
	websocket *websocket.Conn
	waiting   map[string]chan any
	mu        sync.RWMutex
}

func NewRpcClient(websocket *websocket.Conn) *RpcClient {
	return &RpcClient{
		websocket: websocket,
		waiting:   make(map[string]chan any),
	}
}

func (c *RpcClient) CallRemoteProcedure(procedure string, args []any) (any, error) {
	id := generateID()
	resultChan := make(chan any, 1)

	c.mu.Lock()
	c.waiting[id] = resultChan
	c.mu.Unlock()

	request := RpcRequest{
		ID:        id,
		Procedure: procedure,
		Args:      args,
	}

	requestData, err := json.Marshal(request)
	if err != nil {
		return nil, err
	}

	err = c.websocket.WriteMessage(websocket.TextMessage, requestData)
	if err != nil {
		return nil, err
	}

	result := <-resultChan

	if err, ok := result.(error); ok {
		return nil, err
	}

	return result, nil
}

func (c *RpcClient) OnReceive(response map[string]any) error {
	id, ok := response["id"].(string)
	if !ok {
		return errors.New("invalid response: missing id")
	}

	c.mu.Lock()
	defer c.mu.Unlock()

	resultChan, exists := c.waiting[id]
	if !exists {
		return nil
	}

	delete(c.waiting, id)

	if response["error"] == nil {
		resultChan <- response["payload"]
	} else {
		errorData, ok := response["error"].(map[string]any)
		if !ok {
			resultChan <- errors.New("unknown error")
			return nil
		}

		if errorData["is_deskset_error"] == true {
			message, _ := errorData["message"].(string)
			resultChan <- &DesksetError{Message: message}
		} else {
			resultChan <- errors.New("rpc error")
		}
	}

	return nil
}

func generateID() string {
	bytes := make([]byte, 8)
	rand.Read(bytes)
	return hex.EncodeToString(bytes)
}
