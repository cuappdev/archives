# == Schema Information
#
# Table name: notifications
#
#  id                :integer          not null, primary key
#  from              :integer
#  to                :integer
#  notification_type :integer
#  seen              :boolean          default(FALSE)
#

class NotificationsController < ApplicationController
  def getNotifications
    notifications = Notification.where(:to => params[:user_id]) 
    render json: { notifications: notifications }
  end

  def seen
    @notification = Notification.find(params[:notification_id])
    @notification.seenNotification()
    render json: { success: @notification.seen }
  end
end
