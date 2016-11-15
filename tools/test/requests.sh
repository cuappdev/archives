http GET http://localhost:9000/v1/users
http GET http://localhost:9000/v1/episodes
http GET http://localhost:9000/v1/likes
http GET http://localhost:9000/v1/subscriptions
http GET http://localhost:9000/v1/series
http POST http://localhost:9000/v1/likes user_id:=1 episode_id:=1
http POST http://localhost:9000/v1/subscriptions user_id:1 series_id:=1
http DELETE http://localhost:9000/v1/likes/1
http DELETE http://localhost:9000/v1/subscriptions/1
