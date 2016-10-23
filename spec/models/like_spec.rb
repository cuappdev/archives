require 'rails_helper'

RSpec.describe Like, type: :model do

  before (:each) do
    @l = FactoryGirl.create(:like, user_id: 1, post_id: 1)
  end

  it "tests validation of follower id's" do
    expect(@l.valid?).to eq(true)
  end

end
