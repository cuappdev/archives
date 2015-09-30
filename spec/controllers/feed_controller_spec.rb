require 'rails_helper'

describe 'feed#index' do
  before :each do
    auth_user = User.last
    def auth_post(path, params={}, user=User.last)
      session_code = user.session.code
      post path, {session_code: session_code}.merge(params)
    end

    ('A'..'Z').each do |letter|
      auth_post '/posts', {
        song: {
          artist: "#{letter}#{letter.next}#{letter.next.next}",
          track: "#{letter}#{letter}",
          spotify_url: "https://spotify.com"
        }
      }
    end
  end

  def auth_get(path, params = {}, user=User.last)
    get path, {session_code: user.session.code}.merge(params)
  end

  it 'renders all posts' do
    get '/feed'
    p response.body
  end
end