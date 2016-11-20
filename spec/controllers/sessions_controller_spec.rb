# == Schema Information
#
# Table name: sessions
#
#  id         :integer          not null, primary key
#  user_id    :integer
#  code       :string
#  is_active  :boolean
#  created_at :datetime         not null
#  updated_at :datetime         not null
#

require_relative '../rails_helper'

RSpec.describe SessionsController, type: :controller do
  it "creates session using a FB token" do

  end

  it "logs out of existing session" do

  end

  it "does not log out of nonexistent session" do

  end
end
