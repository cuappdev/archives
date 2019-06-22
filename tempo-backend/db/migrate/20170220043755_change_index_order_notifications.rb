class ChangeIndexOrderNotifications < ActiveRecord::Migration
  def change
  	remove_index :notifications, [:from, :to, :notification_type] if index_exists?(:notifications, [:from, :to, :notification_type]) 
  	add_index :notifications, [:to, :from, :notification_type]
  end
end
