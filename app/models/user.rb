# == Schema Information
#
# Table name: users
#
#  id              :integer          not null, primary key
#  name            :string
#  hipster_score   :integer
#  caption         :string
#  follower_count  :integer
#  location_id     :integer
#  created_at      :datetime         not null
#  updated_at      :datetime         not null
#  followers_count :integer          default(0)
#  like_count      :integer          default(0)
#  fbid            :string
#  username        :string
#

class User < ActiveRecord::Base
  has_many :posts, dependent: :destroy
  has_many :relationships, class_name:  "Following",
                                foreign_key: "follower_id",
                                dependent:   :destroy
  has_many :likes
  has_many :following, through: :relationships, source: :followed
  validates :fname, presence: true, length: { maximum: 50 }
  validates :lname, length: {maximum: 50}

  has_one :session

  # Follows a user.
  def follow(other_user)
    relationships.create(followed_id: other_user.id)
    other_user.increment!(:followers_count)
  end

  # Unfollows a user.
  def unfollow(other_user)
    relationships.find_by(followed_id: other_user.id).destroy
    other_user.decrement!(:followers_count)
  end

  # Returns true if the current user is following the other user.
  def following?(other_user)
    following.include?(other_user)
  end
  # Likes a post
  def like(post)
    Like.create(post_id: post.id, user_id: self.id)
    self.increment!(:like_count)
    post.increment!(:like_count)
  end

  #unlike post
  def unlike(post)
    Like.find_by(post_id: post.id, user_id: self.id).destroy
    self.decrement!(:like_count)
    post.decrement!(:like_count)
  end
  # Returns true if the 
  def liked?(post)
    Like.where(post_id: post.id, user_id: self.id).exists?
  end
end
