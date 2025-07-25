# myapp/views.py
import json
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    """View for the main prediction page"""
    return render(request, 'myapp/index.html')

@csrf_exempt # Important for allowing POST requests from your frontend fetch without CSRF token
def save_label_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            predicted_label = data.get('label')

            if not predicted_label:
                return JsonResponse({'message': 'Label is missing in the request body.'}, status=400)

            # --- ADJUSTED FILE PATH LOGIC ---
            # Get the directory of the current file (myapp/views.py)
            current_app_dir = os.path.dirname(os.path.abspath(__file__))

            # Construct the path to the 'data' folder INSIDE 'myapp'
            data_dir = os.path.join(current_app_dir, 'data')

            # Create the 'data' directory if it doesn't exist
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            # Construct the full path to data.txt
            file_path = os.path.join(data_dir, 'data.txt')
            # --- END ADJUSTED FILE PATH LOGIC ---

            file_content = f"{predicted_label};\n"

            try:
                with open(file_path, 'w') as f: # Use 'a' for append
                    f.write(file_content)
                print(f"Successfully wrote '{predicted_label}' to {file_path}")
                return JsonResponse({'message': 'Label successfully saved.'}, status=200)
            except IOError as e:
                print(f"Error writing to file: {e}")
                return JsonResponse({'message': f'Failed to save label: {e}'}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON in request body.'}, status=400)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return JsonResponse({'message': 'An internal server error occurred.'}, status=500)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed for this endpoint.'}, status=405)