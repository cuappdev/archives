class AddRemotePushNotificationsEnabledToUsers < ActiveRecord::Migration
  def change
    add_column :users, :remote_push_notifications_enabled, :boolean, :default => false
  end
end
