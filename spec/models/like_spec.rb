# == Schema Information
#
# Table name: likes
#
#  id         :integer          not null, primary key
#  post_id    :integer
#  user_id    :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#

require 'rails_helper'

RSpec.describe Like, type: :model do

  before (:each) do
    @l = FactoryGirl.create(:like, user_id: 1, post_id: 1)
  end

  it "tests validation of follower id's" do
    expect(@l.valid?).to eq(true)
  end

end
