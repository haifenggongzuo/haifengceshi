from supabase import create_client
import sys

print("Starting test...")
sys.stdout.flush()

try:
    url = 'https://rwlziuinlbazgoajkcme.supabase.co'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3bHppdWlubGJhemdvYWprY21lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUxODAwNjIsImV4cCI6MjA2MDc1NjA2Mn0.Y1KiIiUXmDiDSFYFQLHmyd1Oe86SxSfvHJcKrJmz2gI'
    
    print("Connecting to Supabase...")
    sys.stdout.flush()
    
    client = create_client(url, key)
    
    print("Connected successfully!")
    sys.stdout.flush()
    
    print("Fetching trades...")
    sys.stdout.flush()
    
    response = client.table('trades').select('*').execute()
    
    print("Response received:")
    print(response)
    sys.stdout.flush()

except Exception as e:
    print("Error occurred:")
    print(str(e))
    print("Type:", type(e).__name__)
    import traceback
    print("Traceback:")
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1) 