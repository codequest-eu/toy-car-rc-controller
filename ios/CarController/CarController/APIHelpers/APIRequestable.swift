//
//  APIRequestable.swift
//  CarController
//
//  Created by Małgorzata Dziubich on 02/11/2017.
//  Copyright © 2017 CodeQuest. All rights reserved.
//

import Alamofire

public enum CarControllerAPIResponse {
    case success()
    case failure(String)
}

public enum CarControllerAPIErrorType: Error {
    case networkError404
    case validServerResponseWithError(response: String)
    case internalError
    case parseError
    case jsonDataInconsistencyError
}

public typealias ResponseHander = (CarControllerAPIResponse) -> Void

public protocol APIRequestable {
    func request(_ url: URLRequestConvertible, completionHandler: @escaping ResponseHander)
}

public extension APIRequestable {
    func request(_ url: URLRequestConvertible, completionHandler: @escaping ResponseHander) {
        Alamofire.request(url)
            .responseJSON { (response) in
                guard let statusCode = response.response?.statusCode,
                statusCode == 200 else {
                    if let response = response.response {
                        let formattedError = "We're sorry! Something's going wrong with our server! Contact Karwer! error code: \(response.statusCode)"
                        completionHandler(.failure(formattedError))
                    } else {
                        completionHandler(.failure("We're sorry! Something's going wrong with our server! Contact Karwer!"))
                    }
                    return
                }
                completionHandler(.success())
        }
    }
}
