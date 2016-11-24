# == Schema Information
#
# Table name: users
#
#  id                                :integer          not null, primary key
#  name                              :string
#  hipster_score                     :integer          default(0)
#  caption                           :string
#  followers_count                   :integer          default(0)
#  location_id                       :integer
#  like_count                        :integer          default(0)
#  fbid                              :string
#  username                          :string
#  email                             :string
#  followings_count                  :integer          default(0)
#  created_at                        :datetime         not null
#  updated_at                        :datetime         not null
#  push_id                           :string
#  remote_push_notifications_enabled :boolean          default(TRUE)
#

class User < ActiveRecord::Base
  has_many :posts, dependent: :destroy
  has_many :likes
  has_many :followings
  #validates :name, presence: true, length: { maximum: 50 }
  validate :username_letter
  before_create :default_values
  has_one :session
  has_one :spotify_cred
  validates :fbid, presence: true, uniqueness: {case_sensitive: false}
  validates :username, uniqueness: {case_sensitive: false}

  # Follows a user
  def follow(followed_id)
    followed = User.find(followed_id)
    following = Following.create(follower_id: self.id, followed_id: followed_id)
    if following.valid? || followed.blank?
      User.increment_counter(:followers_count,followed)
      User.increment_counter(:followings_count,self)
    end
    following.valid? || followed.blank? ? true : false
  end


  # Unfollows a user.
  def unfollow(followed_id)
    followed = User.find(followed_id)
    unfollowing = Following.destroy_all(follower_id: self.id, followed_id: followed_id)
    if !unfollowing.blank? || followed.blank?
      User.decrement_counter(:followers_count, followed) unless followed.followers_count == 0
      User.decrement_counter(:followings_count, self) unless self.followings_count == 0
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
    fids = followers_ids
    fids.count < 1 ? [] : User.where('id IN (?)', fids)
    # fids.count < 1 ? [] : User.where('id IN (?)', fids)
  end


  # Returns list of following ids
  def followings_ids
    Following.where(follower_id: self.id).pluck(:followed_id)
  end


  # Returns a list of following
  def following_list
    User.joins("INNER JOIN followings ON followings.followed_id = users.id WHERE followings.follower_id = #{self.id}").select("users.*")
  end

  # Likes a post
  def like(post)
    if post.blank? 
      return false
    end 
    like = Like.create(post_id: post.id, user_id: self.id)
    if like.valid? || post.blank?
      User.increment_counter(:like_count, self)
      Post.increment_counter(:like_count, post)
    end
    like.valid? ? true : false
  end

  # Updates push id
  def update_push_id(push_id)
    self.push_id = push_id
    self.save
  end

  # Updates remote_push_notifications_enabled
  def update_push_notifications_enabled(enabled)
    self.remote_push_notifications_enabled = enabled
    self.save
  end

  # Returns list of song ids
  def my_songs
    SongPost.joins("INNER JOIN posts ON song_posts.post_id = posts.id WHERE posts.user_id = #{self.id}").pluck(:song_id)
  end


  # Returns number of mutual songs with another user
  def mutual_songs (user_id)
    User.exists?(user_id) ? (self.my_songs & User.find(user_id).my_songs).size : 0
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

  def mutual_following_count(fid)
    mutual_following(fid).length
  end

  # grab mutual_followers
  def mutual_following(fid)
    mutual_following = Following.where('follower_id = (?)',fid).pluck(:followed_id) - [self.id]
    followings_ids & mutual_following
  end

  def as_json(options = {})
      if options[:limited]
        exclude = [:followers_count, :followers, :followings_count, :following, :is_following]
        more_hash = {}
      else
        print(options)
        more_hash = {
          name: self.name,
          username: self.username,
          fbid: self.fbid,
          hipster_score: self.hipster_score,
          followers_count: self.followers_count,
          followings_count: self.followings_count,
          is_following: User.exists?(options[:user_id]) ? User.find(options[:user_id]).following?(self.id) : "Didn't pass in user_id",
          mutual_friends: User.exists?(options[:user_id]) ? User.find(options[:user_id]).mutual_following_count(self.id) : 0
        }
        more_hash[:followers] = followers.map { |user| user.as_json(user_id: self.id, include_following: false, include_followers: false) } if options[:include_followers]
        more_hash[:following] = self.following_list.map { |user| user.as_json(include_following: false, include_followers: false) } if options[:include_following]
        # more_hash[:following] = []
      end
      super(except: exclude).merge(more_hash)
  end


  # VALIDATION METHODS
  # Checks username is valid
  def username_letter
    errors[:base] << "The first character of a username must be a letter." unless ((self.username[0,1] =~ /[A-Za-z]/)==0)
  end


  def update_username(u)
    self.username = u
    is_true = valid?
    self.save
    return is_true
  end


  def default_values
    last_id = User.last == nil ? 1 : (User.last.id) + 1
    self.username = "temp_username_#{last_id}"
    self.like_count = 0
    self.followers_count = 0
    self.followings_count = 0
    self.hipster_score = 0
  end



end
