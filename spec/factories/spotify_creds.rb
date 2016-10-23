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

FactoryGirl.define do
  factory :spotify_cred do
    access_token "fake_access_token"
    refresh_token "fake_refresh_token"
    expires_at "99999999999"
    user_id 1
    spotify_id "fake_spotify_id"
    playlist_id "fake_playlist_id"
    end
end
