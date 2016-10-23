# == Schema Information
#
# Table name: users
#
#  id               :integer          not null, primary key
#  name             :string
#  hipster_score    :integer          default(0)
#  caption          :string
#  location_id      :integer
#  created_at       :datetime         not null
#  updated_at       :datetime         not null
#  followers_count  :integer          default(0)
#  like_count       :integer          default(0)
#  fbid             :string
#  username         :string
#  email            :string
#  followings_count :integer          default(0)
#

FactoryGirl.define do
  factory :user do
    fbid "bogus"
    username "valid"
  end
end
