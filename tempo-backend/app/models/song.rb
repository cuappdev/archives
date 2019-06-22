# == Schema Information
#
# Table name: songs
#
#  id            :integer          not null, primary key
#  spotify_url   :string
#  artist        :string
#  track         :string
#  hipster_score :integer
#  created_at    :datetime         not null
#  updated_at    :datetime         not null
#

class Song < ActiveRecord::Base
  has_many :song_posts, class_name: 'SongPost'
  validates :spotify_url, presence: true, uniqueness: {case_sensitive: true}

  # Grab all the posts
  def posts
    Post.joins("INNER JOIN song_posts ON posts.id = song_posts.post_id WHERE song_posts.song_id = #{self.id}").select("posts.*")
  end

  # Count number of users who posted a particular song
  def number_of_users
    posts.pluck(:user_id).count
  end

end
