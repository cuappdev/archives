#!/usr/bin/ruby

Pod::Spec.new do |s|
  s.name             = 'SwiftRegister'
  s.version          = '0.0.2'
  s.summary          = 'register client library for iOS'


  s.description      = <<-DESC
  register client library for iOS
                       DESC

  s.homepage         = 'https://github.com/cuappdev/register-client-ios'
  s.license          = 'MIT'
  s.author           = { 'Cornell AppDev' => 'cornellappdev@gmail.com' }
  s.source           = { :git => 'https://github.com/cuappdev/register-client-ios.git', :tag => 'v'+s.version.to_s }

  s.ios.deployment_target = '10.0'

  s.source_files = 'SwiftRegister/Classes/**/*'

  s.dependency 'PromiseKit', '~> 4.4'
  s.dependency 'PromiseKit/Alamofire'
  s.dependency 'SwiftyJSON'
  s.dependency 'RealmSwift'
  s.dependency 'Log'
end
