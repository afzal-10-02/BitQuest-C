import os
from flask import request
from flask_restful import Resource


class FileHandler(Resource):
    DATA_DIRECTORY = "data"  # Directory for storing files

    def get(self):
        """
        Handles GET requests to check if a file exists.
        Query parameter:
        - file_name: Name of the file to check
        """
        file_name = request.args.get('file_name', '').strip()
        if not file_name:
            return {"message": "Query parameter 'file_name' is required"}, 400

        file_name += '.csv'
        file_path = os.path.join(self.DATA_DIRECTORY, file_name)

        if os.path.exists(file_path):
            return {"message": f"File '{file_name}' exists"}, 200
        else:
            return {"message": f"File '{file_name}' does not exist"}, 404

    def post(self):
        """
        Handles POST requests to create a new file.
        Query parameter:
        - file_name: Name of the file to create
        """
        file_name = request.args.get('file_name', '').strip()
        if not file_name:
            return {"message": "Query parameter 'file_name' is required"}, 400

        file_name += '.csv'
        file_path = os.path.join(self.DATA_DIRECTORY, file_name)

        if os.path.exists(file_path):
            return {"message": "File already exists"}, 400

        # Create the file
        os.makedirs(self.DATA_DIRECTORY, exist_ok=True)
        with open(file_path, mode='w', encoding='utf-8') as file:
            pass

        return {"message": f"File '{file_name}' created successfully"}, 201



    def delete(self):
        
        file_name = request.args.get('file_name', '').strip()
        if not file_name:
            return {"message": "Query parameter 'file_name' is required"}, 400

        file_name += '.csv'
        file_path = os.path.join(self.DATA_DIRECTORY, file_name)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return {"message": f"File '{file_name}' deleted successfully"}, 200
            else:
                return {"message" : f"File {file_name} not Found"}, 404
        except FileNotFoundError:
            return {"message": f"File '{file_name}' not found"}, 404
        except Exception as e:
            return {"message": f"Error deleting file: {str(e)}"}, 500