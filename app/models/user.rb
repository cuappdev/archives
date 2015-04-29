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
  has_many :relationships, class_name:  "Following",
                                foreign_key: "follower_id",
                                dependent:   :destroy
  has_many :likes
  has_many :following, through: :relationships, source: :followed
  # validates :name, presence: true, length: { maximum: 50 }

  has_one :session

  # Follows a user.
  def follow(other_user)
    other_id = other_user.is_a?(User) ? other_user.id : other_user
    relationships.create(follower_id: self.id, followed_id: other_id)
    User.increment_counter(:followers_count, other_id)
  end
  # Unfollows a user.
  def unfollow(other_user)
    other_id = other_user.is_a?(User) ? other_user.id : other_user
    relationships.desroy(follower_id: self.id, followed_id: other_id)
    User.decrement_counter(:followers_count, other_id)
  end

  # Returns true if the current user is following the other user.
  def following?(other_user)
    following.include?(other_user)
  end
  # Returns list of followers
  def followers
    follower_ids = Following.where(followed_id: self.id).pluck(:follower_id)
    follower_ids.count < 1 ? [] : User.where('id in ?', follower_ids)
  end
  # Likes a post
  def like(post)
    post_id = post.is_a?(User) ? post.id : post
    Like.create(post_id: post_id, user_id: self.id)
    self.increment!(:like_count)
    Post.increment_counter(:like_count, post_id)
  end 

  #unlike post
  def unlike(post)
    post_id = post.is_a?(User) ? post.id : post
    Like.destroy(post_id: post_id, user_id: self.id)
    self.decrement!(:like_count)
    Post.decrement_counter(:like_count, post_id)
  end
  # Returns true if the 
  def liked?(post)
    Like.where(post_id: post.id, user_id: self.id).exists?
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
end
