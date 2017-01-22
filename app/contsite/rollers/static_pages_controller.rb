class StaticPagesController < ApplicationController
  include StaticPagesHelper

  def home
  end

  def recruitment
  end

  def training
  end

  def team
    @groupings = load_team
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
