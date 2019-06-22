class CreateSongs < ActiveRecord::Migration
  def change
    create_table :songs do |t|
      t.string :spotify_url
      t.string :artist
      t.string :track
      t.integer :hipster_score

      t.timestamps null: false
    end
  end
end
