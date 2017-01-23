require 'csv'

module StaticPagesHelper

  # Load the team CSV and build an array of members
  def load_team

    # Aggregrate team
    team = Array.new
    team_file = File.join(File.dirname(__FILE__), 'team.csv')
    CSV.foreach(team_file) do |line|
      team << (TeamMember.new line)
    end

    # Group by category
    categories = {}
    team.each do |mem|
      if ! categories.has_key? mem.category
        categories[mem.category] = Array.new
      end
      categories[mem.category] << mem
    end

    # Return grouped member
    categories
  end

  # App Dev Team Member
  class TeamMember

    # Getter methods
    attr_reader :name, :year, :role, :category, :photo, :github, :twitter, :linkedin

    # Expected order is:
    # [name, year, role, category, photo, github, twitter, linkedin]
    def initialize line
      @name = line[0]
      @year = line[1]
      @role = line[2]
      @category = line[3]
      @photo = line[4]
      @github = line[5] != "NONE" ? line[5] : nil
      @twitter = line[6] != "NONE" ? line[6] : nil
      @linkedin = line[7] != "NONE" ? line[7] : nil
    end

  end


end
