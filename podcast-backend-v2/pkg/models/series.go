package models

import (
	"time"
)

// Series is a podcast series
type Series struct {
	Artist      string
	FeedURL     string
	ImageURL    string
	Name        string
	ReleaseDate time.Time
	SeriesID    int
}

// NewSeriesFromSearchResult creates a Series struct from a SearchResultEntry
func NewSeriesFromSearchResult(sre SearchResultEntry) *Series {
	return &Series{
		Name:        sre.CollectionName,
		SeriesID:    sre.CollectionID,
		Artist:      sre.ArtistName,
		FeedURL:     sre.FeedURL,
		ImageURL:    sre.ArtworkURL100,
		ReleaseDate: sre.ReleaseDate}
}
