//
//  CarActionsAPIHelper.swift
//  CarController
//
//  Created by Małgorzata Dziubich on 02/11/2017.
//  Copyright © 2017 CodeQuest. All rights reserved.
//

import Foundation
import Alamofire

class CarActionsAPIHelper: APIRequestable {

    func request(action: ActionType, completion: @escaping (_ success: Bool, _ errorMsg: String?) -> Void) {
        request(APICarActionsRouter(action: action)) { (response) in
            switch response {
            case .success:
                completion(true, nil)
            case .failure(let error):
                completion(false, error)
            }
        }
    }
}
