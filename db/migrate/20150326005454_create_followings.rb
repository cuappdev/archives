class CreateFollowings < ActiveRecord::Migration
  def change
    create_table :followings do |t|
      t.integer :follower_id, references: "user", index: true
      t.integer :followed_id, references: "user", index: true

      t.timestamps null: false
    end
  end
end
