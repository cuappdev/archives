class AddFollowingCountToUsers < ActiveRecord::Migration
  def change
    add_column :users, :followings_count, :integer
  end
end
