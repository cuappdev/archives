package main

import (
	"podcast-backend-v2/pkg/connector"
)

func main() {
	connector.InitializeRedisClient()
}
