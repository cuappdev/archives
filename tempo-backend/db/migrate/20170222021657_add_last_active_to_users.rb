class AddLastActiveToUsers < ActiveRecord::Migration
  def change
  	add_column :users, :last_active, :datetime
  	User.find_each do |user|
  		user.last_active = DateTime.now
  		user.save
  	end
  end
end
