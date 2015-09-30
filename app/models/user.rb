# == Schema Information
#
# Table name: users
#
#  id              :integer          not null, primary key
#  name            :string
#  hipster_score   :integer
#  caption         :string
#  location_id     :integer
#  created_at      :datetime         not null
#  updated_at      :datetime         not null
#  followers_count :integer          default(0)
#  like_count      :integer          default(0)
#  fbid            :string
#  username        :string
#  email           :string
#

class User < ActiveRecord::Base
  has_many :posts, dependent: :destroy
  has_many :likes
  has_many :followings
  # validates :name, presence: true, length: { maximum: 50 }
  before_create :default_values
  has_one :session

  # Follows a user
  def follow(followed_id)
    followed = User.find(followed_id)
    following = Following.create(follower_id: self.id, followed_id: followed_id) 
    if following.valid? || followed.blank?
      User.increment_counter(:followers_count,followed)
    end
    following.valid? || followed.blank? ? true : false
  end

  # Unfollows a user.
  def unfollow(followed_id)
    followed = User.find(followed_id)
    unfollowing = Following.destroy_all(follower_id: self.id, followed_id: followed_id)
    if !unfollowing.blank? || followed.blank?
      User.decrement_counter(:followers_count, followed) unless followed.followers_count == 0
    end
    unfollowing.blank? || followed.blank? ? false : true
  end

  # Returns true if the current user is following the other user.
  def following?(followed_id)
    Following.where(follower_id: self.id, followed_id: followed_id).exists?
  end
  # Returns list of followers ids
  def followers_ids 
    Following.where(followed_id: self.id).pluck(:follower_id)
  end
  # Returns list of followers
  def followers
    followers_ids.count < 1 ? [] : User.where('id IN (?)', followers_ids)
  end
  # Likes a post
  def like(post_id)
    post = Post.find(post_id)
    like = Like.create(post_id: post_id, user_id: self.id) 
    if like.valid? || post.blank?
      User.increment_counter(:like_count,self)
      Post.increment_counter(:like_count,post)
    end
    like.valid? || post.blank? ? true : false
  end 

  #unlike post
  def unlike(post_id)
    post = Post.find(post_id)
    unlike = Like.destroy_all(user_id: self.id, post_id: post_id)
    if !unlike.blank? || post.blank?
      User.decrement_counter(:like_count, self) unless self.like_count == 0
      Post.decrement_counter(:like_count, post) unless post.like_count == 0
    end
    unlike.blank? || post.blank? ? false : true
  end
  # Returns true if the post was liked by the user
  def liked?(post_id)
    Like.where(post_id: post_id, user_id: self.id).exists?
  end
  # Returns a list of ids of liked posts
  def liked_posts_ids
    post_ids = Like.where(user_id: self.id).pluck(:post_id)
  end
  # Returns a list of liked posts
  def liked_posts
    liked_posts_ids.count < 1 ? [] : Post.where('id IN (?)', liked_posts_ids)
  end

  def as_json(options = {})
      more_hash = {
        followers: self.followers,
        name: self.name,
        username: self.username,
        fbid: self.fbid,
        hipster_score: self.hipster_score
      }
      more_hash[:following] = self.following.map { |user| user.as_json(include_followers: false) } if options[:include_followers]
      super().merge(more_hash)
  end
  def default_values
    self.like_count = 0
    self.followers_count = 0
    self.hipster_score = 0
  end
end
