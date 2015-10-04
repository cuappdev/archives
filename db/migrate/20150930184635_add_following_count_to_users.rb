class AddFollowingCountToUsers < ActiveRecord::Migration
  def change
    add_column :users, :followings_count, :integer, default: 0
  end
end
