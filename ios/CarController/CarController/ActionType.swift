//
//  ActionType.swift
//  CarController
//
//  Created by mdziubich on 02/10/2017.
//  Copyright © 2017 CodeQuest. All rights reserved.
//

enum ActionType {
    
    case idle
    case stop
    case freeRemoteRide
//    collectingDataFromCamera,  // nie potrzebujemy w pierwszym rzucie
//    recordingTrackWithoutCamera, // nie potrzebujemy w pierwszym rzucie
    case autonomusMode
//    playingSavedTrack // nie potrzebujemy w pierwszym rzucie
    case changeSpeed(Int)
    
    var statusTitle: String {
        switch self {
        case .idle, .stop:                  return "IDLE"
        case .freeRemoteRide:               return "Free Remote Ride"
//        case .collectingDataFromCamera:     return "Collecting Data From Camera"
//        case .recordingTrackWithoutCamera:  return "Record Track Without Camera"
        case .autonomusMode:                return "Autonomus Ride"
//        case .playingSavedTrack:            return "Playing Saved Track"
        case .changeSpeed:                  return ""
        }
    }
    
    //do not include `changeSpeed` which is not action
    static var allValues: [ActionType] {
        return [.freeRemoteRide,
//                .collectingDataFromCamera,
//                .recordingTrackWithoutCamera,
                .autonomusMode]
//                .playingSavedTrack]
    }
}
