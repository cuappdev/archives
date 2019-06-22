//
//  ViewController.swift
//  SwiftRegisterExample
//
//  Created by Serge-Olivier Amega on 2/1/18.
//  Copyright © 2018 CocoaPods. All rights reserved.
//

import UIKit
import SwiftRegister

let apiUrl = URL(string: "http://52.54.98.130/api/")!
let secret = "6b8b3326418a12a861afe70d31cf540ddf65f7e3"

struct ButtonTapPayload: Payload {
    enum TapKind: String, Codable {
        case tapUp
    }
    
    enum Context: String, Codable {
        case mainVCContext
    }
    
    static let eventName: String = "button_tap"
    let tapKind: TapKind
    let context: Context
    
    private enum CodingKeys: String, CodingKey {
        case tapKind = "tap_kind"
        case context
    }
}

class ViewController: UIViewController {
    
    let session = RegisterSession.init(apiUrl: apiUrl, secretKey: secret, logMode: .regular)
    
    @IBAction func buttonPressedUp(_ sender: Any) {
        session.logEvent(event: ButtonTapPayload(tapKind: .tapUp, context: .mainVCContext).toEvent())
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

