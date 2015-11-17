module FollowingsHelper
  def update_mutual_friends(follow_bool, user, followed_id)
    mutual_followers = Following.where('followed_id = (?)',followed_id).pluck(:follower_id) - [user.id]
    return if mutual_followers.empty?
    if follow_bool
      mutual_followers.do |idx| 
        order = [user.id,idx].sort! {|x,y| x <=> y}
        relation = Mutualfriend.find_or_create_by(user1_id: order.first,user2_id: order.second)
        Mutualfriend.increment_counter(:mutual_friends_count, relation)
      end
    else
      mutual_followers.do |idx|
        order = [user.id,idx].sort! {|x,y| x <=> y}
        relation = Mutualfriend.find_by(user1_id: order.first, user2_id: order.second)
        Mutualfriend.decrement_counter(:mutual_friends_count, relation) if relation.mutual_friends_count != 0 
      end
    end
  end
end
