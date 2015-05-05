# == Schema Information
#
# Table name: posts
#
#  id         :integer          not null, primary key
#  username   :string
#  created_at :datetime         not null
#  updated_at :datetime         not null
#  like_count :integer          default(0)
#  user_id    :integer
#

class Post < ActiveRecord::Base
  belongs_to :user
  has_many :likes

  has_many :song_posts, class_name: 'SongPost'
  # has_many :songs, through: :song_posts
  validates :user_id, presence: true
  validates :like_count, numericality: { greater_than_or_equal_to: 0 }

  def songs
    Song.where(id: SongPost.where(post_id: self.id).pluck(:song_id))
  end

  def as_json(options = {})
    super(options).merge(song: self.songs.first, user: self.user)
  end
end
