# == Schema Information
#
# Table name: song_posts
#
#  id         :integer          not null, primary key
#  post_id    :integer
#  song_id    :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#

FactoryGirl.define do
  factory :songpost do
    song
    post
  end
end
