# == Schema Information
#
# Table name: followings
#
#  id          :integer          not null, primary key
#  follower_id :integer
#  followed_id :integer
#  created_at  :datetime         not null
#  updated_at  :datetime         not null
#

module FollowingsHelper
  def update_mutual_friends(follow_bool, user_id, followed_id)
    mutual_followers = Following.where('followed_id = (?)',followed_id).pluck(:follower_id) - [user_id]
    return if mutual_followers.empty?
    if follow_bool
      mutual_followers.each do |idx| 
        order = [user_id,idx].sort! {|x,y| x <=> y}
        relation = Mutualfriend.find_or_create_by(user1_id: order.first,user2_id: order.second)
        Mutualfriend.increment_counter(:mutual_friends_count, relation)
      end
    else
      mutual_followers.each do |idx|
        order = [user_id,idx].sort! {|x,y| x <=> y}
        relation = Mutualfriend.find_by(user1_id: order.first, user2_id: order.second)
        Mutualfriend.decrement_counter(:mutual_friends_count, relation) if relation.mutual_friends_count != 0 
      end
    end
  end
end
