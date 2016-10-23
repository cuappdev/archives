# == Schema Information
#
# Table name: posts
#
#  id         :integer          not null, primary key
#  like_count :integer          default(0)
#  user_id    :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#

class Post < ActiveRecord::Base
  belongs_to :user
  has_many :likes

  has_many :song_posts, class_name: 'SongPost'
  # has_many :songs, through: :song_posts
  validates :user_id, presence: true
  validates :like_count, :numericality => {:greater_than_or_equal_to => 0}

  before_create :default_values
  def songs
    Song.where(id: SongPost.where(post_id: self.id).pluck(:song_id))
  end

  def as_json(options = {})
      more_hash = {
        like_count: self.like_count,
        is_liked: User.find(options[:id]).liked?(self.id)
      }
    super(options).merge(post: more_hash, song: self.songs.first, user: self.user.as_json(limited: true))
  end
  private
  def default_values
    self.like_count = 0
  end
end
