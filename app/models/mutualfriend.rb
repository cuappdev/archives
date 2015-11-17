# == Schema Information
#
# Table name: mutualfriends
#
#  id                   :integer          not null, primary key
#  user1_id             :integer
#  user2_id             :integer
#  mutual_friends_count :integer
#  created_at           :datetime         not null
#  updated_at           :datetime         not null
#

class Mutualfriend < ActiveRecord::Base
  before_create :default_values
  belongs_to :user1, class_name: "User"
  belongs_to :user2, class_name: "User"
  validates :user1_id, presence: true
  validates :user2_id, presence: true
  validates_numericality_of :user2_id, :greater_than => :user1_id
  def default_values
    self.mutual_friends_count = 0
  end
end
