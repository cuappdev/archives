http GET http://localhost:9000/v1/users
http GET http://localhost:9000/v1/episodes
http POST http://localhost:9000/v1/episodes audiosearch_id:=1 title='Hi' description='Hello' audio_url="http://example.com" image_url="http://example.com" series_id:=0
http GET http://localhost:9000/v1/likes
http POST http://localhost:9000/v1/likes user_id:=1 episode_id:=1
http POST http://localhost:9000/v1/series audiosearch_id:=1 title='Test Series' description='Test' imageUrl='http://example.com/img.jpg'
http POST http://localhost:9000/v1/subscriptions user_id:1 series_id:=1
