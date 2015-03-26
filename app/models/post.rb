# == Schema Information
#
# Table name: posts
#
#  id         :integer          not null, primary key
#  username   :string
#  song_id    :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#  like_count :integer          default(0)
#  user_id    :integer
#

class Post < ActiveRecord::Base
  belongs_to :user
  has_many :likes
  validates :user_id, presence: true
  validates :song_id, presence: true
end
