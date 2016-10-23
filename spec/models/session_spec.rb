require 'rails_helper'

RSpec.describe Session, type: :model do

  before (:each) do
    @s = FactoryGirl.create(:session, user_id: 1, code: "test_session_code")
  end

  it "activate" do
    @s.activate
    expect(@s.is_active).to eq(true)
  end

  it "disable" do
    @s.disable
    expect(@s.is_active).to eq(false)
  end

end
