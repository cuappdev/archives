class CreateSpotifyCreds < ActiveRecord::Migration
  def change
    create_table :spotify_creds do |t|
      t.string :access_token
      t.string :refresh_token
      t.string :expires_at
      t.timestamps null: false
      t.integer :user_id, references: "user", index: true
      t.string :spotify_id
      t.string :playlist_id
    end
  end
end
