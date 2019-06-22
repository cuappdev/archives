# == Schema Information
#
# Table name: followings
#
#  id          :integer          not null, primary key
#  follower_id :integer
#  followed_id :integer
#  created_at  :datetime         not null
#  updated_at  :datetime         not null
#

require 'rails_helper'

RSpec.describe Following, type: :model do

  before (:each) do
    @f = FactoryGirl.create(:following, follower_id: 1, followed_id: 2)
  end

  it "tests validation of following" do
    expect(@f.valid?).to eq(true)
  end

end
