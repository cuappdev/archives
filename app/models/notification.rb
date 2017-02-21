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

class Notification < ActiveRecord::Base
	validates :from, presence: true
	validates :to, presence: true
	validates :notification_type, presence: true
  include HttpHelper

  def seenNotification()
    self.seen = true 
    self.save
  end

  def shouldNotify() 
     # TODO
  end

  def sendNotification()
     # TODO 
  end

end 
