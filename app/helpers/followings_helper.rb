module FollowingsHelper
  def update_mutual_friends(follow_bool, user, followed_id)
    # if following
    mutual_followers = Following.where('followed_id = (?)',followed_id).pluck(:follower_id) - [user.id]
    p '-------------------------'
    p 'mutual followers'
    p mutual_followers
    p '-------------------------'
    return if mutual_followers.empty?
    if follow_bool
      mutual_followers.each { |idx|
        if Mutualfriend.exists?(user2_id: idx)
          relation = Mutualfriend.find_by(user1_id: user.id, user2_id: idx) or Mutualfriend.find_by(user1_id: idx, user2_id: user.id)
          Mutualfriend.increment_counter(:mutual_friends_count, relation)
        else
          Mutualfriend.create(user1_id: user.id, user2_id: idx)
        end
      }
    else
      mutual_followers.each { |idx|
        p '----'
        p 'index'
        p idx
        p '----'
        relation = Mutualfriend.find_by(user1_id: user.id, user2_id: idx) or Mutualfriend.find_by(user1_id: idx, user2_id: user.id)
        Mutualfriend.decrement_counter(:mutual_friends_count, relation) if relation.mutual_friends_count != 0 
      }
    end
  end
end
