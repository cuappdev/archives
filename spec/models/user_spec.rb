# == Schema Information
#
# Table name: users
#
#  id               :integer          not null, primary key
#  name             :string
#  hipster_score    :integer          default(0)
#  caption          :string
#  location_id      :integer
#  created_at       :datetime         not null
#  updated_at       :datetime         not null
#  followers_count  :integer          default(0)
#  like_count       :integer          default(0)
#  fbid             :string
#  username         :string
#  email            :string
#  followings_count :integer          default(0)
#

require 'rails_helper'

RSpec.describe User, type: :model do
 	

 	before(:each) do 
 		@u = FactoryGirl.create(:user, fbid: "bogus", username: "valid")
 	end 


 	it "test validation of username" do 

 		expect(@u.valid?).to eq(true)
 		result = @u.update_username("12notvalid")
 		expect(result).to eq(false)
 		expect(@u.valid?).to eq(false)
 		result = @u.update_username("valid")
 		expect(result).to eq(true)
 		expect(@u.valid?).to eq(true)


 	end 


end
