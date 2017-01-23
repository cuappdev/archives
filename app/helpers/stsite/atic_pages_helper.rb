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

    # Return grouped members
    categories
  end

  # App Dev Team Member
  class TeamMember

    # Getter methods
    attr_reader :name, :year, :role, :category, :photo, :github, :linkedin

    # Expected order is:
    # [name, year, role, category, photo, github, linkedin]
    def initialize line
      @name = line[0]
      @year = line[1]
      @role = line[2]
      @category = line[3]
      @photo = line[4]
      @github = line[5] != "NONE" ? "https://github.com/#{line[5]}" : nil
      @linkedin = line[6] != "NONE" ? "https://www.linkedin.com/in/#{line[6]}" : nil
    end

    # Professional links
    def prof_links
      links = Array.new
      if ! @github.nil?
        links << { link_type: "github", link: @github }
      end
      if ! @linkedin.nil?
        links << { link_type: "linkedin", link: @linkedin }
      end
      links
    end

  end


end
