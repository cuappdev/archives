class CreateMutualfriends < ActiveRecord::Migration
  def change
    create_table :mutualfriends do |t|
      t.integer :user1_id
      t.integer :user2_id
      t.integer :mutual_friends_count

      t.timestamps null: false
    end
  end
end
