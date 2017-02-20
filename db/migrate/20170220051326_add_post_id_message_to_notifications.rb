class AddPostIdMessageToNotifications < ActiveRecord::Migration
  def change
  	add_column :notifications, :post_id, :integer
  	add_column :notifications, :message, :string
  	Notification.find_each do |notification| 
  		if notification.notification_type == 1 #likes 
  			notification.post_id = notification.to
  			post = Post.find(notification.post_id)
  			notification.to = post.user_id
  			track_name = post.songs.first.track
  			username = User.find(:id => notification.from).username
  			notification.message = "@#{username} liked a song you posted: #{track_name}!"
  			notification.save
  		end
  		if notification.notification_type == 2 #follows
  			follower_username = User.find(notification.from).username
  			notification.message = "@#{follower_username} is following you!"
  			notification.save
  		end
  	end
  end
end
