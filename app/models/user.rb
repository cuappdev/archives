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
  validates :name, presence: true, length: { maximum: 50 }

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
  # Returns list of followers
  def followers
    User.where('id in ?', Following.where(followed_id: self.id).pluck(:follower_id))
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
