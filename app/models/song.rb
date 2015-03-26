# == Schema Information
#
# Table name: songs
#
#  id          :integer          not null, primary key
#  spotify_url :string
#  artist      :string
#  track       :string
#  created_at  :datetime         not null
#  updated_at  :datetime         not null
#

class Song < ActiveRecord::Base
  has_many :song_posts, class_name: 'SongPost'

  def posts
    Post.where(id: SongPost.where(song_id: self.id).pluck(:post_id))
  end
end
