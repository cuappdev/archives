class CreateNotifications < ActiveRecord::Migration
  def change
    create_table :notifications do |t|
      t.integer :from
      t.integer :to
      t.integer :notification_type
    end
    add_index :notifications, [:from, :to, :notification_type] 
  end
end
