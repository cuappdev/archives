class CreateSessions < ActiveRecord::Migration
  def change
    create_table :sessions do |t|
      t.integer :user_id
      t.string :code
      t.boolean :is_active

      t.timestamps null: false
    end
  end
end
