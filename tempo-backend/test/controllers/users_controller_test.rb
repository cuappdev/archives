# == Schema Information
#
# Table name: users
#
#  id                                :integer          not null, primary key
#  name                              :string
#  hipster_score                     :integer          default(0)
#  caption                           :string
#  followers_count                   :integer          default(0)
#  location_id                       :integer
#  like_count                        :integer          default(0)
#  fbid                              :string
#  username                          :string
#  email                             :string
#  followings_count                  :integer          default(0)
#  created_at                        :datetime         not null
#  updated_at                        :datetime         not null
#  push_id                           :string
#  remote_push_notifications_enabled :boolean          default(FALSE)
#  last_active                       :datetime
#

require 'test_helper'

class UsersControllerTest < ActionController::TestCase
end
