# == Schema Information
#
# Table name: mutualfriends
#
#  id                   :integer          not null, primary key
#  user1_id             :integer
#  user2_id             :integer
#  mutual_friends_count :integer
#  created_at           :datetime         not null
#  updated_at           :datetime         not null
#

require 'rails_helper'

RSpec.describe Mutualfriend, type: :model do
  pending "add some examples to (or delete) #{__FILE__}"
end
