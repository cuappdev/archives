//
//  RouteTableViewCell.swift
//  The Cat
//
//  Created by Eric Appel on 9/20/15.
//  Copyright © 2015 Eric Appel. All rights reserved.
//

import UIKit
import MapKit

class RouteTableViewCell: UITableViewCell {

    @IBOutlet weak var leftLabel: UILabel!
    @IBOutlet weak var routeLabel: UILabel!
    @IBOutlet weak var rightLabel: UILabel!
    @IBOutlet weak var mapView: MKMapView!
    
    var delegate: MKMapViewDelegate?
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
    func setOption(option: routeOption) {
        leftLabel.text = "\(option.stops.first!.time)-\(option.stops.last!.time)"
        routeLabel.text = "Route \(option.route.id) (\(option.stops.count-1) stops)"
        rightLabel.text = "\(Int(option.stops.last!.date.timeIntervalSinceDate(option.stops.first!.date) / 60)) mins"
        
        mapView.delegate = delegate

        placeStopsOnMap(option.stops)
    }
    
    func placeStopsOnMap(stops: [RouteStop]) {
        var stopModels: [Stop] = []
        for s in stops {
            if let stop = stopsDict[s.stopName] {
                stopModels.append(stop)
                mapView.addAnnotation(stop)
            }
        }
        
        // Find limits
        var upper = stopModels[0].coordinate
        var lower = stopModels[0].coordinate
        
        for s in stopModels {
            if s.coordinate.latitude > upper.latitude { upper.latitude = s.coordinate.latitude }
            if s.coordinate.latitude < lower.latitude { lower.latitude = s.coordinate.latitude }
            if s.coordinate.longitude > upper.longitude { upper.longitude = s.coordinate.longitude }
            if s.coordinate.longitude < lower.longitude { lower.longitude = s.coordinate.longitude }
        }
        
        // Find Region
        var locationSpan = MKCoordinateSpan()
        locationSpan.latitudeDelta = upper.latitude - lower.latitude + 0.05
        locationSpan.longitudeDelta = upper.longitude - lower.longitude + 0.025
        var locationCenter = CLLocationCoordinate2D()
        locationCenter.latitude = (upper.latitude + lower.latitude) / 2
        locationCenter.longitude = (upper.longitude + lower.longitude) / 2
        
        let region = MKCoordinateRegion(center: locationCenter, span: locationSpan)
        mapView.setRegion(region, animated: false)
    }
    
}
