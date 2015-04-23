//
//  PostView.swift
//  IceFishing
//
//  Created by Alexander Zielenski on 4/12/15.
//  Copyright (c) 2015 Alexander Zielenski and Mark Bryan. All rights reserved.
//

import UIKit

class PostView: UIView, UIGestureRecognizerDelegate {
    private var progressGestureRecognizer: UIPanGestureRecognizer?
    var tapGestureRecognizer: UITapGestureRecognizer?
    @IBOutlet var profileNameLabel: MarqueeLabel?
    @IBOutlet var avatarImageView: UIImageView?
    @IBOutlet var descriptionLabel: MarqueeLabel?
    @IBOutlet var dateLabel: UILabel?
    var fillColor = UIColor(red: CGFloat(19.0/255.0), green: CGFloat(39.0/255.0), blue: CGFloat(49.0/255.0), alpha: 1.0)
    private var updateTimer: NSTimer?
    private var notificationHandler: AnyObject?
    
    var post: Post? {
        didSet {
            if let handler: AnyObject = notificationHandler {
                NSNotificationCenter.defaultCenter().removeObserver(handler)
            }
            
            println("got here")
            // update stuff
            if let post = post {
                profileNameLabel?.text = post.posterFirstName + " " + post.posterLastName
                descriptionLabel?.text = post.song.title + " · " + post.song.artist
                avatarImageView?.image = post.avatar
                
                //! TODO: Write something that makes this nice and relative
                //! that updates every minute
                let dateFormatter = NSDateFormatter()
//                dateFormatter.doesRelativeDateFormatting = true
                dateFormatter.dateStyle = .NoStyle
                dateFormatter.timeStyle = .ShortStyle
                dateLabel?.text = dateFormatter.stringFromDate(post.date)
                
                if (updateTimer == nil) {
                    updateTimer = NSTimer(timeInterval: 0.0005,
                        target: self, selector: Selector("timerFired:"),
                        userInfo: nil,
                        repeats: true)
                    NSRunLoop.currentRunLoop().addTimer(updateTimer!, forMode: NSRunLoopCommonModes)
                }
                
                notificationHandler = NSNotificationCenter.defaultCenter().addObserverForName(PlayerDidChangeStateNotification,
                    object: post.player,
                    queue: nil, usingBlock: {
                        [unowned self]
                        (note) -> Void in
                        self.updateProfileLabelTextColor()
                })
            } else {
                updateTimer?.invalidate()
                updateTimer = nil
            }
        }
    }
    
    override func didMoveToWindow() {
        if (progressGestureRecognizer == nil) {
            progressGestureRecognizer = UIPanGestureRecognizer(target: self, action: "changeProgress:")
            progressGestureRecognizer?.delegate = self
            progressGestureRecognizer?.delaysTouchesBegan = true
            addGestureRecognizer(progressGestureRecognizer!)
        }
        
        if (tapGestureRecognizer == nil) {
            tapGestureRecognizer = UITapGestureRecognizer(target: self, action: "postViewPressed:")
            tapGestureRecognizer?.delegate = self
            tapGestureRecognizer?.cancelsTouchesInView = false
            addGestureRecognizer(tapGestureRecognizer!)
        }
        
        avatarImageView?.layer.cornerRadius = avatarImageView!.bounds.size.width / 2
        avatarImageView?.clipsToBounds = true
        userInteractionEnabled = true
        avatarImageView?.userInteractionEnabled = true
        profileNameLabel?.userInteractionEnabled = true
        
        layer.borderColor = UIColor(red: CGFloat(19.0/255.0), green: CGFloat(39.0/255.0), blue: CGFloat(49.0/255.0), alpha: 1.0).CGColor
        layer.borderWidth = CGFloat(0.7)
        
        profileNameLabel?.scrollRate = 0;
        profileNameLabel?.trailingBuffer = 8.0
        descriptionLabel?.scrollRate = 0;
        descriptionLabel?.trailingBuffer = 8.0;
    }
    
    dynamic private func timerFired(timer: NSTimer) {
        self.setNeedsDisplay()
    }
    
    override func layoutSubviews() {
        super.layoutSubviews()
        updateProfileLabelTextColor()
    }
    
    func updateProfileLabelTextColor() {
        if let post = post {
            var color: UIColor!
            var duration = NSTimeInterval(0.3) as NSTimeInterval
            let label = self.profileNameLabel!
            if post.player.isPlaying() {
                color = UIColor(red: CGFloat(181.0/255.0), green: CGFloat(87.0/255.0), blue: CGFloat(78.0/255.0), alpha: 1.0)
                // Will scroll labels
                profileNameLabel?.scrollRate = 100
                descriptionLabel?.scrollRate = 100
            } else {
                color = UIColor.whiteColor()
                // Labels won't scroll
                profileNameLabel?.scrollRate = 0
                descriptionLabel?.scrollRate = 0
            }
            
            if !label.textColor.isEqual(color) {
                UIView.transitionWithView(label, duration: duration, options: UIViewAnimationOptions.TransitionCrossDissolve, animations: { () -> Void in
                    label.textColor = color
                    }, completion: nil)
            }
        }
    }
    
    dynamic func changeProgress(gesture: UIPanGestureRecognizer) {
        if (gesture.state != .Ended) {
            post?.player.pause(false);
        } else {
            post?.player.play(false);
        }
        
        var xTranslation = gesture.locationInView(self).x
        var cellWidth = bounds.width
        
        let progress = Double(xTranslation/cellWidth)
        post?.player.progress = progress
        
        self.setNeedsDisplay()
    }
    
    override func drawRect(rect: CGRect) {
        var progress = 0.0
        if let post = post {
            progress = post.player.progress
        }
        super.drawRect(rect)
        fillColor.setFill()
        CGContextFillRect(UIGraphicsGetCurrentContext(),
            CGRect(x: 0, y: 0,
                width: self.bounds.size.width * CGFloat(progress),
                height: self.bounds.size.height))
    }
    
    override func gestureRecognizerShouldBegin(gestureRecognizer: UIGestureRecognizer) -> Bool {
        if gestureRecognizer == progressGestureRecognizer {
            if let player = post?.player {
                var offsetY:CGFloat = 0.0
                var offsetX:CGFloat = 0.0
                if let superview = self.superview?.superview?.superview as? UIScrollView {
                    offsetY = superview.contentOffset.y
                    offsetX = superview.contentOffset.x
                }
                var translation = self.progressGestureRecognizer?.translationInView(self)
                
                if let translation = translation {
                    return ((fabs(translation.x) > fabs(translation.y)) &&
                        (offsetY == 0.0 && offsetX == 0.0)) &&
                        player.isPlaying()
                }
            }
            return false
        }
        return true
    }
    
    func postViewPressed(sender: UITapGestureRecognizer) {
        if let post = post {
            if post.player.isPlaying() {
                let tapPoint = sender.locationInView(self)
                let hitView = self.hitTest(tapPoint, withEvent: nil)
                
                if hitView == avatarImageView || hitView == self.profileNameLabel {
                    // GO TO PROFILE VIEW CONTROLLER
                    println("GO TO PROFILE")
                }
            }
        }
    }
}
