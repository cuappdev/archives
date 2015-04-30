//
//  FeedVC.swift
//  IceFishingTrending
//
//  Created by Joseph Antonakakis on 3/15/15.
//  Copyright (c) 2015 Joseph Antonakakis. All rights reserved.
//

import UIKit
import MediaPlayer

var addedSongs = 0
class FeedViewController: UITableViewController, UIScrollViewDelegate, SearchTrackResultsViewControllerDelegate, UISearchControllerDelegate {

    lazy var searchResultsController: SearchTrackResultsViewController = SearchTrackResultsViewController()
    lazy var searchController: TrackSearchController = TrackSearchController(searchResultsController: self.searchResultsController)
    var preserveTitleView: UIView!
    
    var posts: [Post] = []
    var currentlyPlayingIndexPath: NSIndexPath? {
        didSet {
            if (currentlyPlayingIndexPath?.isEqual(oldValue) ?? false) { // Same index path tapped
                currentlyPlayingPost?.player.togglePlaying()
            } else { // Different cell tapped
                currentlyPlayingPost?.player.pause(true)
                currentlyPlayingPost?.player.progress = 1.0 // Fill cell as played
                
                if let currentlyPlayingIndexPath = currentlyPlayingIndexPath {
                    currentlyPlayingPost = posts[currentlyPlayingIndexPath.row]
                    currentlyPlayingPost!.player.play(true)
                } else {
                    currentlyPlayingPost = nil
                }
            }
            
            tableView.selectRowAtIndexPath(currentlyPlayingIndexPath, animated: false, scrollPosition: UITableViewScrollPosition.None)
            cellPin()
        }
    }
    var currentlyPlayingPost: Post?
    
    var topPinViewContainer: UIView = UIView()
    var bottomPinViewContainer: UIView = UIView()
    @IBOutlet var pinView: PostView!
    var pinViewGestureRecognizer: UITapGestureRecognizer!
    var lastContentOffset: CGFloat!  //Deals with pinView detection
    
    func addSong(track: Song) {
        posts.append(Post(song: track,
            posterFirst: "Mark",
            posterLast: "Bryan",
            date: NSDate(),
            avatar: UIImage(named: "Sexy")))
        self.tableView.reloadData()
    }
    
    private func updateNowPlayingInfo() {
        let session = AVAudioSession.sharedInstance()
        
        if let post = self.currentlyPlayingPost {
            session.setCategory(AVAudioSessionCategoryPlayback, error: nil)
            session.setActive(true, error: nil)
            
            // state change, update play information
            let center = MPNowPlayingInfoCenter.defaultCenter()
            if (post.player.progress != 1.0) {
                let artwork = post.song.fetchArtwork() ?? UIImage(named: "Sexy")!
                center.nowPlayingInfo = [
                    MPMediaItemPropertyTitle:  post.song.title,
                    MPMediaItemPropertyArtist: post.song.artist,
                    MPMediaItemPropertyAlbumTitle: post.song.album,
                    //!TODO: cache this image
                    MPMediaItemPropertyArtwork: MPMediaItemArtwork(image: artwork),
                    MPMediaItemPropertyPlaybackDuration: post.player.duration,
                    MPNowPlayingInfoPropertyElapsedPlaybackTime: post.player.currentTime,
                    MPNowPlayingInfoPropertyPlaybackRate: post.player.isPlaying() ? post.player.rate : 0.0,
                    MPNowPlayingInfoPropertyPlaybackQueueIndex: currentlyPlayingIndexPath!.row,
                    MPNowPlayingInfoPropertyPlaybackQueueCount: posts.count ]
            } else {
                session.setActive(false, error: nil)
                center.nowPlayingInfo = nil
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        NSNotificationCenter.defaultCenter().addObserverForName(PlayerDidChangeStateNotification, object: nil, queue: nil) { [weak self] (note) -> Void in
            self?.updateNowPlayingInfo()
        }
        
        NSNotificationCenter.defaultCenter().addObserverForName(PlayerDidSeekNotification, object: nil, queue: nil) { [weak self] (note) -> Void in
            self?.updateNowPlayingInfo()
        }
        
        NSNotificationCenter.defaultCenter().addObserverForName(SongDidDownloadArtworkNotification, object: nil, queue: nil) { [weak self] (note) -> Void in
            self?.updateNowPlayingInfo()
        }
        
        NSNotificationCenter.defaultCenter().addObserverForName(PlayerDidFinishPlayingNotification, object: nil, queue: nil) { [weak self] (note) -> Void in
            if let current = self?.currentlyPlayingPost {
                if (current.player == note.object as? Player) {
                    let path = self!.currentlyPlayingIndexPath
                    if let path = path {
                        var row = path.row + 1
                        if (row >= self!.posts.count) {
                            row = 0
                        }
                        
                        self?.currentlyPlayingIndexPath = NSIndexPath(forRow: row, inSection: path.section)
                    }
                }
            }
        }
        
        //!TODO: fetch the largest artwork image for lockscreen in Post
        let center = MPRemoteCommandCenter.sharedCommandCenter()
        center.playCommand.addTargetWithHandler { [weak self] (event) -> MPRemoteCommandHandlerStatus in
            if let player = self?.currentlyPlayingPost?.player {
                player.play(true)
                return .Success
            }
            return .NoSuchContent
        }
        center.pauseCommand.addTargetWithHandler { [weak self] (event) -> MPRemoteCommandHandlerStatus in
            if let player = self?.currentlyPlayingPost?.player {
                player.pause(true)
                return .Success
            }
            return .NoSuchContent
        }
        
        center.nextTrackCommand.addTargetWithHandler { [weak self] (event) -> MPRemoteCommandHandlerStatus in
            if let path = self?.currentlyPlayingIndexPath {
                if (path.row < self!.posts.count - 1) {
                    self?.currentlyPlayingIndexPath = NSIndexPath(forRow: path.row + 1, inSection: path.section)
                    return .Success
                }
            }

            return .NoSuchContent
        }
        
        center.previousTrackCommand.addTargetWithHandler { [weak self] (event) -> MPRemoteCommandHandlerStatus in
            if let path = self?.currentlyPlayingIndexPath {
                if (path.row > 0) {
                    self?.currentlyPlayingIndexPath = NSIndexPath(forRow: path.row - 1, inSection: path.section)
                }
                return .Success
            }

            return .NoSuchContent
        }
        
        center.seekForwardCommand.addTargetWithHandler { [weak self] (event) -> MPRemoteCommandHandlerStatus in
            
            return .Success
        }
        
        center.seekBackwardCommand.addTargetWithHandler { [weak self] (event) -> MPRemoteCommandHandlerStatus in
            
            return .Success
        }
        
        
        //—————————————from MAIN VC——————————————————
        navigationItem.title = "Songs"
        addPlusButton()
        
        navigationController?.navigationBar.barTintColor = UIColor.iceDarkRed()
        navigationController?.navigationBar.tintColor = UIColor.whiteColor()
        navigationController?.navigationBar.barStyle = .Black
        //        navigationController?.navigationBar.translucent = true
        
        // Add hamburger menu to the left side of the navbar
        var menuButton = UIButton(frame: CGRect(x: 0, y: 0, width: 25, height: navigationController!.navigationBar.frame.height * 0.65))
        menuButton.setImage(UIImage(named: "white-hamburger-menu-Icon"), forState: .Normal)
        menuButton.addTarget(self.revealViewController(), action: "revealToggle:", forControlEvents: .TouchUpInside)
        navigationItem.leftBarButtonItem = UIBarButtonItem(customView: menuButton)
        
        // Pop out sidebar when hamburger menu tapped
        if self.revealViewController() != nil {
            self.view.addGestureRecognizer(self.revealViewController().panGestureRecognizer())
        }
        
        // Arbitrary additions for SWRevealVC
        revealViewController().panGestureRecognizer()
        revealViewController().tapGestureRecognizer()
        //—————————————from MAIN VC——————————————————
        
        refreshControl = UIRefreshControl()
        refreshControl?.addTarget(self, action: "refreshFeed", forControlEvents: .ValueChanged)
        refreshControl?.attributedTitle = NSAttributedString(string: "Last Updated on \(NSDate())", attributes: [ NSForegroundColorAttributeName: UIColor.whiteColor() ])
        
        tableView.separatorStyle = .None
        tableView.registerNib(UINib(nibName: "FeedTableViewCell", bundle: nil), forCellReuseIdentifier: "FeedCell")
        
        var post = Post(song: Song(songID: "3TV9xKWFOxndERab4wwxsj"), posterFirst: "Mark", posterLast: "Bryan", date: NSDate(), avatar: UIImage(named: "Sexy"))
        posts.append(post)
        post = Post(song: Song(songID: "3igu6bCzkaIrioZIhK3p2n"), posterFirst: "Eric", posterLast: "Appelaklsdjalskdjaslkdjalskjdalksjdalksjdlkasjdlaskjdlaksjdlaksjdalksjdalksjdlkasjdlaksjdlaksjdlaksjd", date: NSDate(), avatar: UIImage(named: "Eric"))
        posts.append(post)
        post = Post(song: Song(songID: "5Yt80fWRB8JG73XlPjrrKP"), posterFirst: "Steven", posterLast: "Yeh", date: NSDate(), avatar: UIImage(named: "Steven"))
        posts.append(post)
        
        //background color for the view
        self.tableView.backgroundColor = UIColor.iceDarkGray()
        self.tableView.separatorColor = UIColor.iceDarkGray()
        tableView.rowHeight = 80
        pinViewGestureRecognizer = UITapGestureRecognizer(target: self, action: "togglePlay")
        pinViewGestureRecognizer.delegate = pinView
        lastContentOffset = tableView.contentOffset.y
        pinView.backgroundColor = UIColor.iceLightGray()
    }
    
    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        topPinViewContainer.frame = CGRect(x: 0, y: 0, width: view.frame.width, height: 80.0)
        topPinViewContainer.center = CGPoint(x: view.center.x, y: navigationController!.navigationBar.frame.maxY + topPinViewContainer.frame.height/2)
        parentViewController!.view.addSubview(topPinViewContainer)
        bottomPinViewContainer.frame = CGRect(x: 0, y: 0, width: view.frame.width, height: 80.0)
        bottomPinViewContainer.center = CGPoint(x: view.center.x, y: view.frame.height - topPinViewContainer.frame.height/2)
        parentViewController!.view.addSubview(bottomPinViewContainer)
        
        topPinViewContainer.hidden = true
        bottomPinViewContainer.hidden = true
        
        pinView.frame = CGRect(x: 0, y: 0, width: view.frame.width, height: 80.0)
    }
    
    func togglePlay() {
        pinView.post?.player.togglePlaying()
    }
    
    //MARK: - UIRefreshControl
    func refreshFeed() {
        //        testSongIDs.append("https://p.scdn.co/mp3-preview/dba0ce6ac6310d7be00545861f9b58aeb86930a3")
        //        testSongDescriptions.append("Don't Stop the Party - Pitbull")
        var post: Post?
        switch (addedSongs) {
        case 0:
            post = Post(song: Song(songID: "0fgZUSa7D7aVvv3GfO0A1n"), posterFirst: "Eric", posterLast: "Appel", date: NSDate(), avatar: UIImage(named: "Eric"))
            break
        case 1:
            post = Post(song: Song(songID: "5dANgSy7v091dhiPnEXNrf"), posterFirst: "Steven", posterLast: "Yeh", date: NSDate(), avatar: UIImage(named: "Steven"))
            break
        case 2:
            post = Post(song: Song(songID: "4wQrzVXnhslsVY5lZSJjHG"), posterFirst: "Mark", posterLast: "Bryan", date: NSDate(), avatar: UIImage(named: "Sexy"))
            break
        case 3:
            post = Post(song: Song(spotifyURI: "spotify:track:4B3RmT3cGvh8By3WY9pbIx"),
                posterFirst: "Eric",
                posterLast: "Appel",
                date: NSDate(),
                avatar: UIImage(named:"Eric"))
            break
        default:
            post = Post(song: Song(songID: "0nmxH6IsSQVT1YEsCB9UMi"), posterFirst: "Steven", posterLast: "Yeh", date: NSDate(), avatar: UIImage(named: "Steven"))
            break
        }
        
        posts.append(post!)
        addedSongs++
        self.tableView.reloadData()
        self.refreshControl?.endRefreshing()
    }
    
    // MARK: - UITableViewDataSource
    
    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return posts.count
    }
    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCellWithIdentifier("FeedCell", forIndexPath: indexPath) as! FeedTableViewCell
        cell.postView.post = posts[indexPath.row]
        cell.postView.post?.player.prepareToPlay()
        return cell
    }
    
    // MARK: - UITableViewDelegate
    override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        currentlyPlayingIndexPath = indexPath
    }
    
    override func scrollViewDidScroll(scrollView: UIScrollView) {
        cellPin()
        println(tableView.contentOffset.y)
        if var lastCell = NSIndexPath(forRow: posts.count-1, inSection: 0) {
            if (currentlyPlayingIndexPath != nil) {
                var rowsICanSee = tableView.indexPathsForVisibleRows() as! [NSIndexPath]
                if let cellSelected = tableView.cellForRowAtIndexPath(currentlyPlayingIndexPath!) {
                    if (lastCell == currentlyPlayingIndexPath && cellSelected.frame.maxY - tableView.contentOffset.y < parentViewController!.view.frame.height) {
                        if (tableView.contentOffset.y > lastContentOffset) {
                            bottomPinViewContainer.hidden = true
                            println(tableView.frame.height)
                        }
                    }
                }
            }
        }
        lastContentOffset = tableView.contentOffset.y
    }
    
    func cellPin() {
        if let selectedRow = currentlyPlayingIndexPath { //If a row is selected
            let rowsICanSee = tableView.indexPathsForVisibleRows() as! [NSIndexPath] //Rows Seen
            if let cellSelected = tableView.cellForRowAtIndexPath(selectedRow) as? FeedTableViewCell {
                if cellSelected.frame.minY - tableView.contentOffset.y < navigationController!.navigationBar.frame.maxY || rowsICanSee.last == selectedRow { //If the cell is the top or bottom
                    if (cellSelected.frame.minY - tableView.contentOffset.y < navigationController!.navigationBar.frame.maxY) {
                        pinView.post = posts[selectedRow.row]
                        pinView.layoutIfNeeded()
                        topPinViewContainer.addSubview(pinView)
                        pinView.addGestureRecognizer(pinViewGestureRecognizer)
                        topPinViewContainer.hidden = false
                        
                    } else if (cellSelected.frame.maxY - tableView.contentOffset.y > parentViewController!.view.frame.height) {
                        pinView.post = posts[selectedRow.row]
                        pinView.layoutIfNeeded()
                        bottomPinViewContainer.addSubview(pinView)
                        pinView.addGestureRecognizer(pinViewGestureRecognizer)
                        bottomPinViewContainer.hidden = false
                    }
                }
                else {
                    if selectedRow.compare(rowsICanSee.first!) != selectedRow.compare(rowsICanSee.last!) { //If they're equal then the thing is not on screen
                        topPinViewContainer.hidden = true
                        bottomPinViewContainer.hidden = true
                        pinView.post = nil
                        pinView.removeFromSuperview()
                    }
                }
            }
        }
    }
    
    // From Old Main VC, might need some cleanup
    
    func addPlusButton() {
        // Add plus sign to the right side of the navbar
        let button = UIBarButtonItem(barButtonSystemItem: UIBarButtonSystemItem.Add, target: self, action: "initializePostCreation")
        navigationItem.rightBarButtonItem = button
    }
    
    func initializePostCreation() {
        searchResultsController.parent = self
        searchResultsController.shouldResume = currentlyPlayingPost?.player.isPlaying() ?? false
        searchController.searchResultsUpdater = searchResultsController
        searchController.delegate = self
        searchController.parent = self
        searchResultsController.delegate = self
        definesPresentationContext = true
        searchController.searchBar.searchBarStyle = .Minimal
        
        preserveTitleView = navigationItem.titleView
        navigationItem.titleView = searchController.searchBar
        navigationItem.rightBarButtonItem = nil
        
        delay(0.05) {
            self.searchController.searchBar.becomeFirstResponder()
        }
        
    }
    
    func willDismissSearchController(searchController: UISearchController) {
        searchResultsController.finishSearching()
        navigationItem.titleView = preserveTitleView
        addPlusButton()
    }
    
    func selectSong(track: Song) {
        searchController.showResultSelection(track)
    }
    
    func postSong(track: Song) {
        closeSearchView()
        addSong(track)
        searchController.active = false
        
        println("TODO: add this track")
        println(track)
    }
    
    func closeSearchView() {
        searchController.searchBar.text = ""
        searchController.searchBar.resignFirstResponder()
        searchResultsController.finishSearching()
    }
    
    override func canBecomeFirstResponder() -> Bool {
        return true
    }
}
