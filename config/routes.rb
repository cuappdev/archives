Rails.application.routes.draw do
  post 'users/register_push' => "users#register_push"
  post 'users/valid_username' => 'users#valid_username'
  get 'users/valid_fbid' => 'users#valid_fbid'
  post 'users/authenticate' => 'sessions#create'
  post 'users/logout' => 'sessions#logout'

  post 'users' => 'users#create'
  put 'users/:id/toggle_push' => "users#toggle_push"
  put 'users/:id' => 'users#update'
  put 'notifications/:notification_id' => 'notifications#seen'

  post 'posts' => 'posts#create'

  post 'likes' => 'likes#create'
  delete 'likes' => 'likes#destroy'

  get 'feed' => 'feed#index'

  post 'sessions' => 'sessions#create'

  post 'followings' => 'followings#create'
  delete 'followings' => 'followings#destroy'

  get 'users/:id/posts' => 'users#posts'
  get 'users/:id/likes' => 'users#likes'
  get 'users/:id/following' => 'users#following'
  get 'users/:id/followers' => 'users#followers'
  get 'users/:id' => 'users#show'
  get 'users' => 'users#index'
  post 'likes/is_liked' => 'likes#is_liked'
  post 'users/suggestions' => 'users#user_suggestions'
  get 'spotify/get_hash' => 'spotify#get_hash'
  get 'spotify/get_access_token' => 'spotify#get_access_token'
  get 'notifications/:user_id' => 'notifications#getNotifications'

end
