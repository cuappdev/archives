Rails.application.routes.draw do

  resources :friends
  post 'users/valid_username' => 'users#valid_username'
  get 'users/valid_fbid' => 'users#valid_fbid'
  post 'users/authenticate' => 'sessions#create'
  post 'users/logout' => 'sessions#logout'

  resources :users
  resources :posts
  resources :likes
  resources :feed
  resources :sessions
  resources :followings

  post 'likes' => 'likes#create'
  delete 'likes' => 'likes#destroy'

  post 'followings' => 'followings#create'
  delete 'followings' => 'followings#destroy'

  get 'users/:id/posts' => 'users#posts'
  get 'users/:id/likes' => 'users#likes'
  get 'users/:id/following' => 'users#following'
  get 'users/:id/followers' => 'users#followers'
  post 'likes/is_liked' => 'likes#is_liked'
  post 'users/suggestions' => 'users#user_suggestions'
  get 'spotify/get_hash' => 'spotify#get_hash'
  get 'spotify/get_access_token' => 'spotify#get_access_token'
  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".

  # You can have the root of your site routed with "root"
  # root 'welcome#index'

  # Example of regular route:
  #   get 'products/:id' => 'catalog#view'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

  # Example resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Example resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Example resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Example resource route with more complex sub-resources:
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', on: :collection
  #     end
  #   end

  # Example resource route with concerns:
  #   concern :toggleable do
  #     post 'toggle'
  #   end
  #   resources :posts, concerns: :toggleable
  #   resources :photos, concerns: :toggleable

  # Example resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end
end
