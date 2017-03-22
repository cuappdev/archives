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

class NotificationsController < ApplicationController
  def getNotifications
    page_length = params[:l].blank? ? 5 : (params[:l]).to_i
    page = params[:p].blank? ? 0 : (params[:p]).to_i 
    
    notifications = Notification.where(:to => params[:user_id]).order('id DESC').slice(page * page_length, page_length).as_json

    render json: { notifications: notifications }
  end

  def seen
    @notification = Notification.find(params[:notification_id])
    @notification.seenNotification()
    render json: { success: @notification.seen }
  end
end
