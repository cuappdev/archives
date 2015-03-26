class CreateSongs < ActiveRecord::Migration
  def change
    create_table :songs do |t|
      t.integer :post_id
      t.string :spotify_url
      t.string :artist
      t.string :track

      t.timestamps null: false
    end
  end
end
