class AddIsActiveToSessions < ActiveRecord::Migration
  def change
    add_column :sessions, :is_active, :boolean
  end
end
