class User < ActiveRecord::Base

  validates :email, presence: true, uniqueness: true
  validate :has_proper_email, :on => :create

  def has_proper_email
    result = !((self.email =~ /\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i).nil?)
    if !result
      errors[:base] << ("Please enter a valid email")
    end
  end

end
