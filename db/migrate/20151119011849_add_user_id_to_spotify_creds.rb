class AddUserIdToSpotifyCreds < ActiveRecord::Migration
  def change
    add_column :spotify_creds, :user_id, :integer
  end
end
