//
//  APIRequestBuilder.swift
//  CarController
//
//  Created by Małgorzata Dziubich on 02/11/2017.
//  Copyright © 2017 CodeQuest. All rights reserved.
//

import Foundation
import Alamofire

public protocol APIUrlPath {
    var path: String { get }
    var method: HTTPMethod { get }
}

public protocol APIRequestBuilder {
    var baseURL: String { get }
    func carAPIRequest() -> URLRequest
}

public extension APIRequestBuilder where Self: APIUrlPath {
    
    var baseURL: String {
        return "http://192.168.1.49:8080"
    }
    
    func carAPIRequest() -> URLRequest {
        let url = URL(string: baseURL)!
        var request = URLRequest(url: url.appendingPathComponent(path))
        request.httpMethod = method.rawValue
        return request
    }
}
