class StaticPagesController < ApplicationController

	def home 
		email = params[:email]
		@user = User.create({ email: email })
		data = @user.valid? ? @user : { error: @user.errors.full_messages }
		respond_to do |f|
			f.html 
			f.json { render json: { success: @user.valid?, data: data }}
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

	def contact 
	end 

	


end
