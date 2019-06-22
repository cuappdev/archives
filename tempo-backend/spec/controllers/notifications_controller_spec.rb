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
#  created_at        :datetime         not null
#  updated_at        :datetime         not null
#

require 'rails_helper'

RSpec.describe NotificationsController, type: :controller do

  describe "GET #getNotifications" do
    it "returns http success" do
      get :getNotifications
      expect(response).to have_http_status(:success)
    end
  end

end
