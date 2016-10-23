require 'rails_helper'

RSpec.describe Post, type: :model do

  before (:each) do
    @p = FactoryGirl.create(:post, like_count: 0, user_id: 1)
  end

  it "tests validation of post" do
    expect(@p.valid?).to eq(true)
    @p.like_count = -1
    expect(@p.valid?).to eq(false)
  end

end
