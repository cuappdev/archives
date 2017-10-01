#!/usr/bin/ruby

Pod::Spec.new do |s|
  s.name             = 'SwiftRegister'
  s.version          = '1.0'
  s.summary          = 'register client library for iOS'


  s.description      = <<-DESC
  register client library for iOS
                       DESC

  s.homepage         = 'https://github.com/cuappdev/register'
  s.license          = 'MIT'
  s.author           = { 'Cornell AppDev' => 'cornellappdev@gmail.com' }
  s.source           = { :git => 'https://github.com/cuappdev/register.git', :tag => 'SwiftRegister-v'+s.version.to_s }

  s.ios.deployment_target = '11.0'

  s.source_files = 'SwiftRegister/Classes/**/*'

  s.dependency 'PromiseKit', '~> 4.4'
  s.dependency 'PromiseKit/Alamofire'
  s.dependency 'SwiftyJSON'
  
end
