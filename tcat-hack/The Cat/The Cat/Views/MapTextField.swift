//
//  MapTextField.swift
//  The Cat
//
//  Created by Eric Appel on 9/19/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit

//let kTextFieldEdgeInset: CGFloat = 20

protocol TextSearchDelegate {
    func startFieldSearch()
    func endFieldSearch()
}

class MapTextField: UIView {
    
    @IBOutlet weak var startTextField: UITextField!
    @IBOutlet weak var endTextField: UITextField!
    
    @IBOutlet weak var startUnderlineView: UIView!
    @IBOutlet weak var endUnderlineView: UIView!
    
    var delegate: TextSearchDelegate?
    
    override func awakeFromNib() {
        startUnderline = startUnderlineView
        endUnderline = endUnderlineView
    }

    @IBAction func startSearchButtonPressed(sender: UIButton) {
        if let d = delegate {
            d.startFieldSearch()
        }
    }
    @IBAction func endSearchButtonPressed(sender: UIButton) {
        if let d = delegate {
            d.endFieldSearch()
        }
    }

    @IBAction func swapButtonPressed(sender: UIButton) {
        let temp = endTextField.text
        endTextField.text = startTextField.text
        startTextField.text = temp
    }
}
