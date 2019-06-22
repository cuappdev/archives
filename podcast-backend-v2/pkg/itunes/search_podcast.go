package itunes

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
)

const (
	podcastSearchURL = "https://itunes.apple.com/search?term=%v&entity=podcast&limit=%v"
)

// MakePodcastSearchRequest searches itunes for Series with name seriesName and returns the payload of the request.
func MakePodcastSearchRequest(seriesName string, limit int) ([]byte, error) {
	searchEndpoint := fmt.Sprintf(podcastSearchURL, url.QueryEscape(seriesName), limit)
	resp, err := http.Get(searchEndpoint)
	if err != nil {
		return nil, fmt.Errorf("an error occurred making the request to itunes :%v", err)
	}

	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("an error occurred making the request to itunes : received status code %v", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("an error occurred parsing the response body :%v", err)
	}

	return body, nil
}
