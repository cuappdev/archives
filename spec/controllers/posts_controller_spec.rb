
# == Schema Information
#
# Table name: posts
#
#  id         :integer          not null, primary key
#  like_count :integer          default(0)
#  user_id    :integer
#  created_at :datetime         not null
#  updated_at :datetime         not null
#

RSpec.describe PostsController, type: :controller do
  it "creates song post given song data" do

  end
end
