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
        case .freeRide: return ""
        case .collectingDataFromCamera: return ""
        case .recordingTrackWithoutCamera: return ""
        case .autonomusMode: return ""
        case .playingSavedTrack: return ""
        }
    }
    
    public func asURLRequest() throws -> URLRequest {
        let  request = carAPIRequest()
//        let urlParams = "?test=TEST&test=TEST"
        return request
    }
}

extension APICarActionsRouter: APIRequestBuilder {}
