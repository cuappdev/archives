# == Schema Information
#
# Table name: songs
#
#  id          :integer          not null, primary key
#  spotify_url :string
#  artist      :string
#  track       :string
#  created_at  :datetime         not null
#  updated_at  :datetime         not null
#

require 'test_helper'

class SongTest < ActiveSupport::TestCase
  # test "the truth" do
  #   assert true
  # end
end
