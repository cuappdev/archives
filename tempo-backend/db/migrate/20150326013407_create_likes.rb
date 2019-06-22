class CreateLikes < ActiveRecord::Migration
  def change
    create_table :likes do |t|
      t.integer :post_id, references: "post", index: true
      t.integer :user_id

      t.timestamps null: false
    end
  end
end
