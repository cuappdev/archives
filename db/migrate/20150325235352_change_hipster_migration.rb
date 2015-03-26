class ChangeHipsterMigration < ActiveRecord::Migration
  def change
    rename_column :users, :hipstore_score, :hipster_score
  end
end
