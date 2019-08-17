# == Schema Information
#
# Table name: spotify_creds
#
#  id            :integer          not null, primary key
#  access_token  :string
#  refresh_token :string
#  expires_at    :string
#  created_at    :datetime         not null
#  updated_at    :datetime         not null
#  user_id       :integer
#  spotify_id    :string
#  playlist_id   :string
#

class SpotifyCred < ActiveRecord::Base
  belongs_to :user
  validates :access_token, presence: true
  validates :refresh_token, presence: true
  validates :expires_at, presence: true
  validates :spotify_id, presence: true

  def update_playlist(playlist_id)
      self.playlist_id = playlist_id
      self.save
  end

  def update_username(username)
      if (username)
          self.spotify_id = username
          return true
      end
      return false
  end
end