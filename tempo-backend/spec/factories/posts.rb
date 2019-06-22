# == Schema Information
#
# Table name: posts
#
#  id         :integer          not null, primary key
#  like_count :integer          default(0)
#  user_id    :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#  views      :integer
#

FactoryGirl.define do
  factory :post do
    like_count 0
    user_id 1
  end
end
