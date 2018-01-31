Rails.application.routes.draw do

	root to: 'static_pages#home'
	post "home" => "static_pages#home", :as => "home" # For listserv
	get "recruitment" => "static_pages#recruitment", :as => "recruitment"
	get "courses" => "static_pages#courses", :as => "courses"
	get "team" => "static_pages#team", :as => "team"
	get "apply" => "static_pages#apply", :as => "apply"
	get "projects" => "static_pages#projects", :as => "projects"
	get "contact" => "static_pages#contact", :as => "contact"


end
