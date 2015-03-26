class CreateUsers < ActiveRecord::Migration
  def change
    create_table :users do |t|
      t.string :username
      t.string :fname
      t.string :lname
      t.integer :hipstore_score

      t.timestamps null: false
    end
  end
end
