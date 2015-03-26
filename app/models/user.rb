# == Schema Information
#
# Table name: users
#
#  id            :integer          not null, primary key
#  username      :string
#  fname         :string
#  lname         :string
#  hipster_score :integer
#  created_at    :datetime         not null
#  updated_at    :datetime         not null
#

class User < ActiveRecord::Base
  has_many :posts, dependent: :destroy
  has_many :likes
  has_many :relationships, class_name:  "Following",
                                foreign_key: "follower_id",
                                dependent:   :destroy
  has_many :following, through: :relationships, source: :followed
  validates :fname, presence: true, length: { maximum: 50 }
  validates :lname, length: {maximum: 50}


    # Follows a user.
  def follow(other_user)
    relationships.create(followed_id: other_user.id)
  end

  # Unfollows a user.
  def unfollow(other_user)
    relationships.find_by(followed_id: other_user.id).destroy
  end

  # Returns true if the current user is following the other user.
  def following?(other_user)
    following.include?(other_user)
  end
  # validate :should_not_have_profanities

  # BAD_WORDS = %w(cunt shit pussy faggot fuck fuq hoes hoez jizz nigger nigga motherfucker motherfucka mfucka fucka fucker fuckity fck)
  
  # def is_profane_name?(name)
  #   if name.blank?
  #     return false
  #   else
  #     n = name.downcase
  #   end
  #   BAD_WORDS.each do |t|
  #     if n.include? t
  #       return true
  #     end
  #   end
  #   return false
  # end
  # def should_not_have_profanities
  #   if is_profane_name? fname or is_profane_name? lname
  #     errors.add(:name, "shouldn't contain profanities")
  #   end
  # end

  def as_json()
  end


end
