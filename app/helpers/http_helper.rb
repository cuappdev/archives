module HttpHelper
  def post(headers, body, url)
    uri = URI.parse(url)
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    request = Net::HTTP::Post.new(uri.request_uri, headers)
    request.body = body
    response = http.request(request)
    return JSON.parse(response.body)
  end
  
  def get(headers, body, url)
    uri = URI.parse(url)
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE
    request = Net::HTTP::Get.new(uri.request_uri, headers)
    request.body = body
    response = http.request(request)
    return JSON.parse(response.body)
  end
end
