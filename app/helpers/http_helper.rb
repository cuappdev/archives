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

  def post_no_ssl(headers, body, url)
    uri = URI.parse(url)
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = false
    print "hello"
    request = Net::HTTP::Post.new(uri.request_uri, headers)
    print "bye"
    request.body = body
    response = http.request(request)
    print response
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
