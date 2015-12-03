class CreateSpotifyCreds < ActiveRecord::Migration
  def change
    create_table :spotify_creds do |t|
      t.string :access_token
      t.string :refresh_token
      t.string :expires_at
      t.timestamps null: false
    end
  end
end
