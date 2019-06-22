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

FactoryGirl.define do
  factory :song do
    spotify_url "http://example.com"
    artist "fake"
    track "phony"
    hipster_score 9001
  end
end
