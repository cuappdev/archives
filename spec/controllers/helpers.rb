require 'rails_helper'

def extract_response resp
  r = { response: resp, print: true, success: true }
  check_response(r)
end
