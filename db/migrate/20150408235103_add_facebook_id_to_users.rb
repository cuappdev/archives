class AddFacebookIdToUsers < ActiveRecord::Migration
  def change
    add_column :users, :fbid, :string
  end
end
