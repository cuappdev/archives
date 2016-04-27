# == Schema Information
#
# Table name: sessions
#
#  id         :integer          not null, primary key
#  user_id    :integer
#  code       :string
#  created_at :datetime         not null
#  updated_at :datetime         not null
#  is_active  :boolean
#

require 'test_helper'

class SessionTest < ActiveSupport::TestCase
  # test "the truth" do
  #   assert true
  # end
end
