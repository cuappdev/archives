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

require 'rails_helper'

RSpec.describe SpotifyCred, type: :model do

  before (:each) do
    @u = FactoryGirl.create(:user, fbid: "bogus", username: "valid")
    @sc = FactoryGirl.create(:spotify_cred, user_id: @u.id)
  end

  it "tests validation of spotify creds" do
    old_access_token = @sc.access_token
    old_refresh_token = @sc.refresh_token
    old_expires_at = @sc.expires_at
    old_spotify_id = @sc.spotify_id
    expect(@sc.valid?).to eq(true)

    @sc.access_token = nil
    expect(@sc.valid?).to eq(false)
    @sc.access_token = old_access_token

    @sc.refresh_token = nil
    expect(@sc.valid?).to eq(false)
    @sc.refresh_token = old_refresh_token

    @sc.expires_at = nil
    expect(@sc.valid?).to eq(false)
    @sc.expires_at = old_expires_at

    @sc.spotify_id = nil
    expect(@sc.valid?).to eq(false)
    @sc.spotify_id = old_spotify_id
  end

  it "tests update playlist" do
    @sc.update_playlist("test")
    expect(@sc.playlist_id).to eq("test")
  end

  it "tests update username not nil" do
    @sc.update_username("test")
    expect(@sc.spotify_id).to eq("test")
  end

  it "tests update username nil" do
    old_spotify_id = @sc.spotify_id
    @sc.update_username(nil)
    expect(@sc.spotify_id).to eq(old_spotify_id)
  end

end
