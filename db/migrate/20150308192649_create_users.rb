class CreateUsers < ActiveRecord::Migration
  def change
    create_table :users do |t|
      t.string :name
      t.integer :hipster_score
      t.string :caption
      t.integer :follower_count
      t.integer :location_id

      t.timestamps null: false
    end
    add_index :users, :name
    add_index :users, :location_id
  end
end
