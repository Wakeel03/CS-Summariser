from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    @app.route('/', methods=['GET'])
    def get(self):
        data = {
            'users': [
                'Wakeel'
            ]
        }
        # data = pd.read_csv('users.csv')  # read CSV
        # data = data.to_dict()  # convert dataframe to dictionary
        return {'data': data}, 200  # return data and 200 OK code
    
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)
        
        args = parser.parse_args()  # parse arguments to dictionary

        if args['userId'] in list(data['userId']):
            return {
                'message': f"'{args['userId']}' already exists."
            }, 401
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'userId': args['userId'],
                'name': args['name'],
                'city': args['city'],
                'locations': [[]]
            })
            # read our CSV
            data = pd.read_csv('users.csv')
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            # save back to CSV
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200  # return data with 200 OK
    
    def put(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('location', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('users.csv')
        
        if args['userId'] in list(data['userId']):
            # evaluate strings of lists to lists
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )
            # select our user
            user_data = data[data['userId'] == args['userId']]

            # update user's locations
            user_data['locations'] = user_data['locations'].values[0] \
                .append(args['location'])
            
            # save back to CSV
            data.to_csv('users.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the userId does not exist
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404
    
    def delete(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add userId arg
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv('users.csv')
        
        if args['userId'] in list(data['userId']):
            # remove data entry matching given userId
            data = data[data['userId'] != args['userId']]
            
            # save back to CSV
            data.to_csv('users.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        else:
            # otherwise we return 404 because userId does not exist
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404


class Locations(Resource):
    def get(self):
        data = 'Hello Locations'
        # data = pd.read_csv('users.csv')  # read CSV
        # data = data.to_dict()  # convert dataframe to dictionary
        return {'data': data}, 200  # return data and 200 OK code
    
    def patch(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('locationId', required=True, type=int)  # add args
        parser.add_argument('name', store_missing=False)  # name/rating are optional
        parser.add_argument('rating', store_missing=False)
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv('locations.csv')
        
        # check that the location exists
        if args['locationId'] in list(data['locationId']):
            # if it exists, we can update it, first we get user row
            user_data = data[data['locationId'] == args['locationId']]
            
            # if name has been provided, we update name
            if 'name' in args:
                user_data['name'] = args['name']
            # if rating has been provided, we update rating
            if 'rating' in args:
                user_data['rating'] = args['rating']
            
            # update data
            data[data['locationId'] == args['locationId']] = user_data
            # now save updated data
            data.to_csv('locations.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        
        else:
            # otherwise we return 404 not found
            return {
                'message': f"'{args['locationId']}' location does not exist."
            }, 404

    
#localhost:5000
api.add_resource(Users, '/')  # '/users' is our entry point for Users

if __name__ == '__main__':
    app.run()  # run our Flask ap
