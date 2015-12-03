# == Schema Information
#
# Table name: spotify_creds
#
#  id            :integer          not null, primary key
#  access_token  :string
#  refresh_token :string
#  expires_at    :string
#  created_at    :datetime         not null
#  updated_at    :datetime         not null
#  user_id       :integer
#

class SpotifyCred < ActiveRecord::Base
  belongs_to :user
  validates :access_token, presence: true
  validates :refresh_token, presence: true
  validates :expires_at, presence: true
end
