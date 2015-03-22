# == Schema Information
#
# Table name: users
#
#  id             :integer          not null, primary key
#  name           :string
#  hipster_score  :integer
#  caption        :string
#  follower_count :integer
#  location_id    :integer
#  created_at     :datetime         not null
#  updated_at     :datetime         not null
#

class User < ActiveRecord::Base
end
