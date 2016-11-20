# == Schema Information
#
# Table name: users
#
#  id               :integer          not null, primary key
#  name             :string
#  hipster_score    :integer          default(0)
#  caption          :string
#  followers_count  :integer          default(0)
#  location_id      :integer
#  like_count       :integer          default(0)
#  fbid             :string
#  username         :string
#  email            :string
#  followings_count :integer          default(0)
#  created_at       :datetime         not null
#  updated_at       :datetime         not null
#  push_id          :string
#  active           :boolean          default(TRUE)
#

FactoryGirl.define do
  factory :user do
    fbid "bogus"
    username "valid"
  end
end
