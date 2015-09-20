//
//  StopTableViewCell.swift
//  The Cat
//
//  Created by Eric Appel on 9/20/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

class StopTableViewCell: UITableViewCell {

    @IBOutlet weak var stopNameLabel: UILabel!
    @IBOutlet weak var distanceLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
    func setStop(stop: Stop, distanceString: String) {
        stopNameLabel.text = stop.name
        distanceLabel.text = distanceString
    }
    
}
