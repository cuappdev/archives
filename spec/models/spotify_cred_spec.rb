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
#  spotify_id    :string
#  playlist_id   :string
#

require 'rails_helper'

RSpec.describe SpotifyCred, type: :model do
  pending "add some examples to (or delete) #{__FILE__}"
end
