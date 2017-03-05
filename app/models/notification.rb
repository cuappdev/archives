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
     inactiveUsersToNotify = inactiveUsers.where(:remote_push_notifications_enabled => true)
     defaultMsg = "Seems like you have been inactive for a couple days... Come back and share a song or two! :)"
     inactiveUsersToNotify.each do |user|
     #### TODO: remove duplicate code ####
     sqlQuery = "(SELECT posts.* FROM posts INNER JOIN followings ON (followings.follower_id = %i AND posts.user_id = followings.followed_id) WHERE posts.created_at >= NOW() - '1 day'::INTERVAL UNION SELECT * FROM posts WHERE posts.user_id = %i AND posts.created_at >= NOW() - '1 day'::INTERVAL) ORDER BY created_at DESC;" % [user.id, user.id]
     queryResult = Post.find_by_sql(sqlQuery)
     #### above gets the posts in your current feed #### 
     msg = defaultMsg
     if queryResult.length > 0 
       msg = "You have #{queryResult.length} new song suggestions from your friends on Tempo!"
     end
     if queryResult.length == 0
       randomNumber = rand(3)
       case randomNumber
       when 0
         msg = "Have a song you’ve been listening to recently? Share it on Tempo"
       when 1
         msg = "Your followers miss you. Post today!"
       else
         msg = "What are you listening to?"
     end  
     Notification.create(to: user.id, notification_type: 100, message: msg)
     LikesController.helpers.notify([user.push_id], msg, 100)
   end
  end
end 
