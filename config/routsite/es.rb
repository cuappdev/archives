Rails.application.routes.draw do
  
	root to: 'static_pages#home'
	post "home" => "static_pages#home", :as => "home" # For listserv 
	get "recruitment" => "static_pages#recruitment", :as => "recruitment"
	get "training" => "static_pages#training", :as => "training"
	get "team" => "static_pages#team", :as => "team"
	get "apply" => "static_pages#apply", :as => "apply"
	get "projects" => "static_pages#projects", :as => "projects"
	get "legal" => "static_pages#legal", :as => "legal"
	get "contact" => "static_pages#contact", :as => "contact"
	get "idea" => "static_pages#idea", :as => "idea"
	get "sponsors" => "static_pages#sponsors", :as => "sponsors"

	


end
