class AddCreatedAtToNotifications < ActiveRecord::Migration
  def change
    add_timestamps(:notifications) 
    Notification.find_each do |notification|
      notification.created_at = DateTime.now
      notification.updated_at = DateTime.now 
      notification.save 
    end
    change_column_null :notifications, :created_at, false 
    change_column_null :notifications, :updated_at, false
  end
end
