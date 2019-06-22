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

require 'test_helper'

class SongPostTest < ActiveSupport::TestCase
  # test "the truth" do
  #   assert true
  # end
end
