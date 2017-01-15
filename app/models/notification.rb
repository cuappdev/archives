# == Schema Information
#
# Table name: notifications
#
#  id                :integer          not null, primary key
#  from              :integer
#  to                :integer
#  notification_type :integer
#
class Notification < ActiveRecord::Base
	validates :from, presence: true
	validates :to, presence: true
	validates :notification_type, presence: true
	belongs_to :from, class_name: "User"
	belongs_to :to, class_name: "User"
end 
