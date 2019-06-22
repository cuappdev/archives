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

  def notify(ids, message, notification_type)
    url = "http://35.163.179.243:8080/push"
    headers = {'Content-Type' =>'application/json'}
    body = {:app => "TEMPO",
            :message =>  message, 
            :target_ids => ids,
            :notification => notification_type}
    res = post_no_ssl(headers, body.to_json, url)
  end
end
