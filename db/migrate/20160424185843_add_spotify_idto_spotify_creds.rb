class AddSpotifyIdtoSpotifyCreds < ActiveRecord::Migration
  def change
      add_column :spotify_creds, :spotify_id, :string
      add_column :spotify_creds, :playlist_id, :string
  end
end
