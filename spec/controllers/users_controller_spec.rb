# == Schema Information
#
# Table name: users
#
#  id               :integer          not null, primary key
#  name             :string
#  hipster_score    :integer          default(0)
#  caption          :string
#  location_id      :integer
#  created_at       :datetime         not null
#  updated_at       :datetime         not null
#  followers_count  :integer          default(0)
#  like_count       :integer          default(0)
#  fbid             :string
#  username         :string
#  email            :string
#  followings_count :integer          default(0)
#

require 'rails_helper'

describe ArtistsController do
  describe 'GET index' do
    context 'in JSON format' do
      context 'without a search query' do
        before :each do
          @artist_list = FactoryGirl.create_list :artist, 5
          @artist_list.each_with_index { |a, index| a.score = index; a.save }
          get :index, format: :json
          @artists = JSON.parse(response.body)['artists']
        end
        it 'finds all artists' do
          sorted_artist_ids = @artist_list.map(&:id).reverse
          expect(@artists.map { |artist| artist['id'] }).to eq sorted_artist_ids
        end
      end
      def do_search(query)
        @artist_list = FactoryGirl.create_list(:artist, 2) + FactoryGirl.create_list(:skizzy, 1)
        get :index, q: 'skizzy mars', format: :json
        @artists = JSON.parse(response.body)['artists']
      end
      context 'with a fully matching search query' do
        before(:each) { do_search 'Skizzy Mars' }
        it 'finds the target artist' do
          expect(@artists.first['artist_name']).to eq 'Skizzy Mars'
        end
        it 'does not return irrelevant artists' do
          expect(@artists.count).to eq 1
        end
      end
      context 'with a initial-match search query' do
        before(:each) { do_search 'skizzy' }
        it 'finds the target artist' do
          expect(@artists.first['artist_name']).to eq 'Skizzy Mars'
        end
        it 'does not return irrelevant artists' do
          expect(@artists.count).to eq 1
        end
      end
      context 'with a case insensitive search query' do
        before(:each) { do_search 'skizzy' }
        it 'finds the target artist' do
          expect(@artists.first['artist_name']).to eq 'Skizzy Mars'
        end
        it 'does not return irrelevant artists' do
          expect(@artists.count).to eq 1
        end
      end
      # context 'with a middle-match search query' do
      #   before(:each) { do_search 'not skizzy here' }
      #   it 'does not find the target artist' do
      #     expect(@artists.count).to eq 0
      #   end
      # end
      # context 'with an end-match search query' do
      #   before(:each) { do_search 'mars skizzy' }
      #   it 'does not find the target artist' do
      #     expect(@artists.count).to eq 0
      #   end
      # end
    end
  end
  describe 'POST create' do
    let(:user) { FactoryGirl.create :user }
    def post_artist(artist_name=nil, send_json=false)
      format = send_json ? :json : :html
      post :create, { artist: { artist_name: artist_name }, user_id: user.id }, format: format
    end
    before :each do
      set_login
    end
    after :each do
      ActionMailer::Base.deliveries.clear
    end
    context 'with valid name' do
      it 'creates a new artist' do
        expect {
          post_artist('An artist')
        }.to change(Artist, :count).by(1)
      end
      it 'creates a profile link' do
        expect {
          post_artist('An artist')
        }.to change(ProfileLink, :count).by(1)
      end
      it 'creates an artist profile link' do
        post_artist('An artist')
        expect(ProfileLink.last.target_type).to eq 'artist'
      end
      it 'sends an email' do
        post_artist('An artist')
        expect(ActionMailer::Base.deliveries.count).to eq(1)
      end
      it 'sends an email to the artist' do
        post_artist('An artist')
        expect(ActionMailer::Base.deliveries.first.to).to eq([user.email])
      end
      it 'sends a welcome email with the right subject' do
        post_artist('An artist')
        expect(ActionMailer::Base.deliveries.first.subject).to eq('Welcome to Tunetap, glad to have you onboard!')
      end
      it 'redirects to artist profile' do
        post_artist('An artist')
        expect(response).to redirect_to edit_artist_path(Artist.last)
      end
    end
    context 'with no name' do
      it 'does not create a new artist' do
        expect {
          post_artist
        }.to change(Artist, :count).by(0)
      end
      it 'does not create a profile link' do
        expect {
          post_artist
        }.to change(ProfileLink, :count).by(0)
      end
      it 'does not send an email' do
        post_artist
        expect(ActionMailer::Base.deliveries.count).to eq(0)
      end
    end
    context 'with no user id' do
      def post_with_no_user_id(artist_name)
        post :create, artist: { artist_name: artist_name }, format: :html
      end
      it 'does not create a profile link' do
        expect {
          post_with_no_user_id('Artist')
        }.to change(ProfileLink, :count).by(0)
      end
      it 'does not send an email' do
        post_with_no_user_id('Artist')
        expect(ActionMailer::Base.deliveries.count).to eq(0)
      end
    end
  end
end
