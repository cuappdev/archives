Rails.application.routes.draw do

  post 'users/valid_username' => 'users#valid_username'
  get 'users/valid_fbid' => 'users#valid_fbid'
  post 'users/authenticate' => 'sessions#create'
  post 'users/logout' => 'sessions#logout'

  get 'users' => 'users#index'
  get 'users' => 'users#show'
  post 'users' => 'users#create'
  put 'users' => 'users#update'

  post 'posts' => 'posts#create'

  post 'likes' => 'likes#create'
  delete 'likes' => 'likes#destroy'

  get 'feed' => 'feed#index'

  post 'sessions' => 'sessions#create'

  post 'followings' => 'followings#create'
  delete 'followings' => 'followings#destroy'

  get 'notify' => 'likes#notify'

  get 'users/:id/posts' => 'users#posts'
  get 'users/:id/likes' => 'users#likes'
  get 'users/:id/following' => 'users#following'
  get 'users/:id/followers' => 'users#followers'
  post 'likes/is_liked' => 'likes#is_liked'
  post 'users/suggestions' => 'users#user_suggestions'
  get 'spotify/get_hash' => 'spotify#get_hash'
  get 'spotify/get_access_token' => 'spotify#get_access_token'

end