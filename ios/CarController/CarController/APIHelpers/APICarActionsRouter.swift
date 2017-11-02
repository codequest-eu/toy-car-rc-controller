//
//  APICarActionsRouter.swift
//  CarController
//
//  Created by Małgorzata Dziubich on 02/11/2017.
//  Copyright © 2017 CodeQuest. All rights reserved.
//

import Foundation
import Alamofire

struct APICarActionsRouter: URLRequestConvertible, APIUrlPath {

    var action: ActionType
    
    var method: HTTPMethod {
        return .get
    }
    
    var path: String {
        switch action {
        case .idle: return "/idle"
        case .stop: return "/stop"
        case .freeRemoteRide: return "/remote"
//        case .collectingDataFromCamera: return "/learning" //in the future
//        case .recordingTrackWithoutCamera: return "" //in the future
        case .autonomusMode: return "/drive"
//        case .playingSavedTrack: return "" //replay - nie potrzebujemy w pierwszym rzucie //in the future
        case .changeSpeed(let speed): return "/speed?value=\(speed)"

            //info: start - start recording i stop nagrywa dla replpaya
        }
    }
    
    public func asURLRequest() throws -> URLRequest {
        return carAPIRequest()
    }
}

extension APICarActionsRouter: APIRequestBuilder {}
