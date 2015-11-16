class AddHipsterScoreToSongs < ActiveRecord::Migration
  def change
    add_column :songs, :hipster_score, :int
  end
end
