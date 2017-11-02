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
        case .freeRemoteRide: return "/remote" //zmienić nazwę
//        case .collectingDataFromCamera: return "/learning"
//        case .recordingTrackWithoutCamera: return ""
        case .autonomusMode: return "/drive"
//        case .playingSavedTrack: return "" //replay - nie potrzebujemy w pierwszym rzucie
        case .changeSpeed(let speed): return "/speed?value=\(speed)"

            //start - start recording i stop nagrywa dla replpaya
        }
    }
    
    public func asURLRequest() throws -> URLRequest {
        let  request = carAPIRequest()
//        let urlParams = "?test=TEST&test=TEST"
        return request
    }
}

extension APICarActionsRouter: APIRequestBuilder {}
