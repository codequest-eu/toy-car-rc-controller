//
//  ActionStatus.swift
//  CarController
//
//  Created by mdziubich on 02/10/2017.
//  Copyright © 2017 CodeQuest. All rights reserved.
//

enum ActionType {
    
    case idle,
    freeRide,
    collectingDataFromCamera,
    recordingTrackWithoutCamera,
    autonomusMode,
    playingSavedTrack
    
    var statusTitle: String {
        switch self {
        case .idle:                         return "IDLE"
        case .freeRide:                     return "Free Ride"
        case .collectingDataFromCamera:     return "Collecting Data From Camera"
        case .recordingTrackWithoutCamera:  return "Record Track Without Camera"
        case .autonomusMode:                return "Autonomus Ride"
        case .playingSavedTrack:            return "Playing Saved Track"
        }
    }
    
    static var allValues: [ActionType] {
        return [.idle,
                .freeRide,
                .collectingDataFromCamera,
                .recordingTrackWithoutCamera,
                .autonomusMode,
                .playingSavedTrack]
    }
}
