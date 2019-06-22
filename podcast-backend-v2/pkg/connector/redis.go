package connector

import (
	"github.com/go-redis/redis"
)

// RedisClient is the client used to communicate with redis
var RedisClient *redis.Client

// InitializeRedisClient initializes the RedisClient in the connector package.
// Panics upon failure.
func InitializeRedisClient() {
	client := redis.NewClient(&redis.Options{
		Addr:     "redis:6379",
		Password: "",
		DB:       0,
	})

	_, err := client.Ping().Result()
	if err != nil {
		panic(err)
	}
	RedisClient = client
}
