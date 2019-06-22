package models

import (
	"fmt"
	"testing"
)

func TestNewSearchResult(t *testing.T) {
	var searchResultTests = []struct {
		searchPayload    []byte
		numSearchResults int
		expectingError   bool
		err              error
	}{
		{[]byte(invalidResultJSON), 0, true, fmt.Errorf("")},
		{[]byte(noResultJSON), 0, false, nil},
		{[]byte(oneResultJSON), 1, false, nil},
		{[]byte(twoResultJSON), 2, false, nil},
		{[]byte(missingFieldsResultJSON), 1, false, nil},
		{[]byte(extraFieldJSON), 1, false, nil},
		{[]byte(validationCheck), 0, true, fmt.Errorf("")},
	}

	for _, searchResultTest := range searchResultTests {
		searchResult, err := NewSearchResult(searchResultTest.searchPayload)
		if searchResultTest.expectingError {
			if err == nil {
				t.Fatalf("Expected error %v but received no error", searchResultTest.err)
			}
		} else {
			if searchResultTest.numSearchResults != searchResult.ResultCount {
				t.Fatalf("Expected %v results but received %v results", searchResultTest.numSearchResults, searchResult.ResultCount)
			}
		}

	}

}

var invalidResultJSON = "This is an invalid JSON"

var noResultJSON = `{
 "resultCount":0,
 "results": []
}`

var oneResultJSON = `{
         "resultCount":1,
         "results": [
        {"wrapperType":"track", "kind":"podcast", "collectionId":591291102, "trackId":591291102, "artistName":"a", "collectionName":"a", "trackName":"a", "collectionCensoredName":"a", "trackCensoredName":"a", "collectionViewUrl":"https://itunes.apple.com/us/podcast/a/id591291102?mt=2&uo=4", "feedUrl":"http://j2cool2012.podomatic.com/rss2.xml", "trackViewUrl":"https://itunes.apple.com/us/podcast/a/id591291102?mt=2&uo=4", "artworkUrl30":"https://is1-ssl.mzstatic.com/image/thumb/Music62/v4/83/e8/7c/83e87c4b-94ff-b294-d83a-84433a4fc313/source/30x30bb.jpg", "artworkUrl60":"https://is1-ssl.mzstatic.com/image/thumb/Music62/v4/83/e8/7c/83e87c4b-94ff-b294-d83a-84433a4fc313/source/60x60bb.jpg", "artworkUrl100":"https://is1-ssl.mzstatic.com/image/thumb/Music62/v4/83/e8/7c/83e87c4b-94ff-b294-d83a-84433a4fc313/source/100x100bb.jpg", "collectionPrice":0.00, "trackPrice":0.00, "trackRentalPrice":0, "collectionHdPrice":0, "trackHdPrice":0, "trackHdRentalPrice":0, "releaseDate":"2013-08-17T06:41:00Z", "collectionExplicitness":"explicit", "trackExplicitness":"explicit", "trackCount":5, "country":"USA", "currency":"USD", "primaryGenreName":"Comedy", "contentAdvisoryRating":"Explicit", "artworkUrl600":"https://is1-ssl.mzstatic.com/image/thumb/Music62/v4/83/e8/7c/83e87c4b-94ff-b294-d83a-84433a4fc313/source/600x600bb.jpg", "genreIds":["1303", "26"], "genres":["Comedy", "Podcasts"]}]
        }`

var twoResultJSON = `{
         "resultCount":2,
         "results": [
        {"wrapperType":"track", "kind":"podcast", "collectionId":591291102, "trackId":591291102, "artistName":"a", "collectionName":"a", "trackName":"a", "collectionCensoredName":"a", "trackCensoredName":"a", "collectionViewUrl":"https://itunes.apple.com/us/podcast/a/id591291102?mt=2&uo=4", "feedUrl":"http://j2cool2012.podomatic.com/rss2.xml", "trackViewUrl":"https://itunes.apple.com/us/podcast/a/id591291102?mt=2&uo=4", "artworkUrl30":"https://is1-ssl.mzstatic.com/image/thumb/Music62/v4/83/e8/7c/83e87c4b-94ff-b294-d83a-84433a4fc313/source/30x30bb.jpg", "artworkUrl60":"https://is1-ssl.mzstatic.com/image/thumb/Music62/v4/83/e8/7c/83e87c4b-94ff-b294-d83a-84433a4fc313/source/60x60bb.jpg", "artworkUrl100":"https://is1-ssl.mzstatic.com/image/thumb/Music62/v4/83/e8/7c/83e87c4b-94ff-b294-d83a-84433a4fc313/source/100x100bb.jpg", "collectionPrice":0.00, "trackPrice":0.00, "trackRentalPrice":0, "collectionHdPrice":0, "trackHdPrice":0, "trackHdRentalPrice":0, "releaseDate":"2013-08-17T06:41:00Z", "collectionExplicitness":"explicit", "trackExplicitness":"explicit", "trackCount":5, "country":"USA", "currency":"USD", "primaryGenreName":"Comedy", "contentAdvisoryRating":"Explicit", "artworkUrl600":"https://is1-ssl.mzstatic.com/image/thumb/Music62/v4/83/e8/7c/83e87c4b-94ff-b294-d83a-84433a4fc313/source/600x600bb.jpg", "genreIds":["1303", "26"], "genres":["Comedy", "Podcasts"]},
        {"wrapperType":"track", "kind":"podcast", "collectionId":382503248, "trackId":382503248, "artistName":"A", "collectionName":"MAR☆BINのPodcast!!!", "trackName":"MAR☆BINのPodcast!!!", "collectionCensoredName":"MAR☆BINのPodcast!!!", "trackCensoredName":"MAR☆BINのPodcast!!!", "collectionViewUrl":"https://itunes.apple.com/us/podcast/mar-bin%E3%81%AEpodcast/id382503248?mt=2&uo=4", "feedUrl":"http://www.we-are-a.com/Site/A_Marbin/rss.xml", "trackViewUrl":"https://itunes.apple.com/us/podcast/mar-bin%E3%81%AEpodcast/id382503248?mt=2&uo=4", "artworkUrl30":"https://is4-ssl.mzstatic.com/image/thumb/Music6/v4/00/83/44/008344f6-7d9f-2031-39c1-107020839411/source/30x30bb.jpg", "artworkUrl60":"https://is4-ssl.mzstatic.com/image/thumb/Music6/v4/00/83/44/008344f6-7d9f-2031-39c1-107020839411/source/60x60bb.jpg", "artworkUrl100":"https://is4-ssl.mzstatic.com/image/thumb/Music6/v4/00/83/44/008344f6-7d9f-2031-39c1-107020839411/source/100x100bb.jpg", "collectionPrice":0.00, "trackPrice":0.00, "trackRentalPrice":0, "collectionHdPrice":0, "trackHdPrice":0, "trackHdRentalPrice":0, "releaseDate":"2010-12-25T06:34:00Z", "collectionExplicitness":"cleaned", "trackExplicitness":"cleaned", "trackCount":5, "country":"USA", "currency":"USD", "primaryGenreName":"Music", "contentAdvisoryRating":"Clean", "artworkUrl600":"https://is4-ssl.mzstatic.com/image/thumb/Music6/v4/00/83/44/008344f6-7d9f-2031-39c1-107020839411/source/600x600bb.jpg", "genreIds":["1310", "26"], "genres":["Music", "Podcasts"]}]
        }`

var missingFieldsResultJSON = `{
         "resultCount":1,
         "results": [
        {"collectionId":591291102, "artistName":"a", "collectionName":"a", "feedUrl":"http://j2cool2012.podomatic.com/rss2.xml", "artworkUrl100":"https://is1-ssl.mzstatic.com/image/thumb/Music62/v4/83/e8/7c/83e87c4b-94ff-b294-d83a-84433a4fc313/source/100x100bb.jpg", "releaseDate":"2013-08-17T06:41:00Z"}]
        }`

var extraFieldJSON = `{
         "resultCount":1,
         "results": [
        {"collectionId":591291102, "IrrelevantField1":"1", "IrrelevantField2":"2", "artistName":"a", "collectionName":"a", "feedUrl":"http://j2cool2012.podomatic.com/rss2.xml", "artworkUrl100":"https://is1-ssl.mzstatic.com/image/thumb/Music62/v4/83/e8/7c/83e87c4b-94ff-b294-d83a-84433a4fc313/source/100x100bb.jpg", "releaseDate":"2013-08-17T06:41:00Z"}]
        }`

var validationCheck = `{
         "resultCount":1,
         "results": [
        {"releaseDate":"2013-08-17T06:41:00Z"}]
        }`
