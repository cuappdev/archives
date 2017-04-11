class AddCreatedAtToNotifications < ActiveRecord::Migration
  def change
    #add_column :notifications, :created_at, :datetime, null:false
    #add_column :notifications, :updated_at, :datetime, null:false
    add_timestamps(:notifications, null: false)
  end
end
