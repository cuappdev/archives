package models

import (
	"encoding/json"
	"fmt"
	"time"

	"gopkg.in/go-playground/validator.v9"
)

// A SearchResult is the result returned by a search through the itunes search api
type SearchResult struct {
	ResultCount int                 `json:"resultCount"`
	Results     []SearchResultEntry `json:"results" validate:"dive"`
}

// A SearchResultEntry is the an element that is returned by a search through the itunes search api
type SearchResultEntry struct {
	ArtistID               string    `json:"artistId,omitempty"`
	ArtistName             string    `json:"artistName,omitempty" validate:"required"`
	ArtworkURL30           string    `json:"artworkUrl30,omitempty"`
	ArtworkURL60           string    `json:"artworkUrl60,omitempty"`
	ArtworkURL100          string    `json:"artworkUrl100,omitempty" validate:"required"`
	ArtworkURL600          string    `json:"artworkUrl600,omitempty"`
	ArtistViewURL          string    `json:"artistViewUrl,omitempty"`
	CollectionCensoredName string    `json:"collectionCensoredName,omitempty"`
	CollectionExplicitness string    `json:"collectionExplicitness,omitempty"`
	CollectionHdPrice      int       `json:"collectionHdPrice,omitempty"`
	CollectionID           int       `json:"collectionId,omitempty" validate:"gt=0"`
	CollectionName         string    `json:"collectionName,omitempty" validate:"required"`
	CollectionPrice        float64   `json:"collectionPrice,omitempty"`
	CollectionViewURL      string    `json:"collectionViewUrl,omitempty"`
	ContentAdvisoryRating  string    `json:"contentAdvisoryRating,omitempty"`
	Country                string    `json:"country,omitempty"`
	Currency               string    `json:"currency,omitempty"`
	FeedURL                string    `json:"feedUrl,omitempty" validate:"required,url"`
	GenreIds               []string  `json:"genreIds,omitempty"`
	Genres                 []string  `json:"genres,omitempty"`
	Kind                   string    `json:"kind,omitempty"`
	PrimaryGenreName       string    `json:"primaryGenreName,omitempty"`
	ReleaseDate            time.Time `json:"releaseDate,omitempty" validate:"required"`
	TrackCensoredName      string    `json:"trackCensoredName,omitempty"`
	TrackCount             int       `json:"trackCount,omitempty"`
	TrackExplicitness      string    `json:"trackExplicitness,omitempty"`
	TrackHdPrice           int       `json:"trackHdPrice,omitempty"`
	TrackHdRentalPrice     int       `json:"trackHdRentalPrice,omitempty"`
	TrackID                int       `json:"trackId,omitempty"`
	TrackName              string    `json:"trackName,omitempty"`
	TrackPrice             float64   `json:"trackPrice,omitempty"`
	TrackRentalPrice       int       `json:"trackRentalPrice,omitempty"`
	TrackViewURL           string    `json:"trackViewUrl,omitempty"`
	WrapperType            string    `json:"wrapperType,omitempty"`
}

// NewSearchResult converts the payload of an itunes search request into a SearchResult struct
func NewSearchResult(searchPayload []byte) (*SearchResult, error) {
	searchResult := SearchResult{}
	err := json.Unmarshal(searchPayload, &searchResult)
	if err != nil {
		return nil, fmt.Errorf("an error parsing the search result JSON: %v", err)
	}

	validate := validator.New()
	err = validate.Struct(searchResult)
	if err != nil {
		validationError := err.(validator.ValidationErrors).Error()
		return nil, fmt.Errorf("an error validating the the search result object: %v ", validationError)
	}

	return &searchResult, nil
}
