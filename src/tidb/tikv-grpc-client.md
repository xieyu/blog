# TiKV GRPC Client

## Client

```go
// Client is a client that sends RPC.
// It should not be used after calling Close().
type Client interface {
	// Close should release all data.
	Close() error
	// SendRequest sends Request.
	SendRequest(ctx context.Context, addr string, req *tikvrpc.Request, timeout time.Duration) (*tikvrpc.Response, error)
}
```

## SendRequest

![](./dot/tikv-grpc-client-SendRequest.svg)
