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

require 'test_helper'

class UserTest < ActiveSupport::TestCase
  # test "the truth" do
  #   assert true
  # end
end
