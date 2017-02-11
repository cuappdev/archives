class FeedController < ApplicationController
  before_action :authorize, only: [:index]
  def index
  	sqlQuery = "(SELECT posts.* FROM posts INNER JOIN followings ON (followings.follower_id = %i AND posts.user_id = followings.followed_id) WHERE posts.created_at >= NOW() - '1 day'::INTERVAL UNION SELECT * FROM posts WHERE posts.user_id = %i AND posts.created_at >= NOW() - '1 day'::INTERVAL) ORDER BY created_at DESC;" % [@user.id, @user.id]
    queryResult = Post.find_by_sql(sqlQuery);
    posts = queryResult.map { |post| post.as_json(id: @user.id) }
    render json: { "posts": posts}
  end
end
