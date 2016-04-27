# == Schema Information
#
# Table name: posts
#
#  id         :integer          not null, primary key
#  username   :string
#  created_at :datetime         not null
#  updated_at :datetime         not null
#  like_count :integer          default(0)
#  user_id    :integer
#

require 'test_helper'

class PostsControllerTest < ActionController::TestCase
  # test "the truth" do
  #   assert true
  # end
end
