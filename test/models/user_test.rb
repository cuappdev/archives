# == Schema Information
#
# Table name: users
#
#  id            :integer          not null, primary key
#  username      :string
#  fname         :string
#  lname         :string
#  hipster_score :integer
#  created_at    :datetime         not null
#  updated_at    :datetime         not null
#

require 'test_helper'

class UserTest < ActiveSupport::TestCase
  # test "the truth" do
  #   assert true
  # end
end
