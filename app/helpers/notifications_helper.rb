# == Schema Information
#
# Table name: notifications
#
#  id                :integer          not null, primary key
#  from              :integer
#  to                :integer
#  notification_type :integer
#  seen              :boolean          default(FALSE)
#  post_id           :integer
#  message           :string
#

module NotificationsHelper
end
