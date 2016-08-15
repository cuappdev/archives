require 'mailchimp'
class StaticPagesController < ApplicationController

	

	def home 
		email = params[:email]
		@user = User.create({ email: email })
		result = @user.valid?
		data = result ? @user : { error: @user.errors.full_messages }

		mailchimp = Mailchimp::API.new(ENV["MAILCHIMP_API_KEY"])
		# Conditionally add to general mailing list 
		if result 
			begin  
				mailchimp.lists.subscribe(ENV["CUAPPDEV_INFO_LIST_ID"], { "email" => @user.email }) 
			rescue Mailchimp::ListAlreadySubscribedError
				data = { error: "You're already subscribed to our mailing list" }
				result = false 
			end 
		end 

		respond_to do |f|
			f.html 
			f.json { render json: { success: result, data: data }}
		end 

	end 

	def recruitment
	end 

	def training
	end 

	def team 
	end 

	def apply
	end 

	def projects
	end 

	def legal
	end 

	def idea
	end 

	def contact 
	end 

	


end
