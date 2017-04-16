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
#  created_at        :datetime         not null
#  updated_at        :datetime         not null
#

class Notification < ActiveRecord::Base
	validates :from, presence: true
	validates :to, presence: true
	validates :notification_type, presence: true

  def seenNotification()
    self.seen = true 
    self.save
  end

  def self.notifyAllUsers(msg)
    usersToNotify = User.where(:remote_push_notifications_enabled => true).pluck(:push_id)
    LikesController.helpers.notify(usersToNotify, msg, 100)
  end

  def self.notifyInactiveUsers(num_days)
     inactiveUsers = User.where('last_active < :x_days_ago',
     :x_days_ago => DateTime.now - num_days.days)
    # inactiveUsersToNotify = inactiveUsers.where(:remote_push_notifications_enabled => true)
     inactiveUsersToNotify = inactiveUsers.where(:remote_push_notifications_enabled => true).pluck(:push_id)
     randomNumber = Random.rand(3)
     msg = "Have a song you've been listening to recently? Share it on Tempo!" 
     case randomNumber
      when 0
        msg = "Have a song you've been listening to recently? Share it on Tempo!"
      when 1
        msg = "What are you listening to?"
      else
        msg = "Your followers miss you. Post today!"
     end
     LikesController.helpers.notify(inactiveUsersToNotify, msg, 100)
  end

  def as_json(options = {}) 
    data = {
      type: self.notification_type,
      to: self.to,
      from: User.find(self.from).as_json,
      post_id: self.post_id 
    }

    json = {
      id: self.id,
      message: self.message, 
      generic: self.notification_type != 1 && self.notification_type != 2,
      data: data,
      seen: self.seen, 
      updated_at: self.updated_at
    }
    return json
  end
end
