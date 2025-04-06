from app import create_app
import sys

app = create_app()

if __name__ == '__main__':
    port = 5000
    if len(sys.argv) > 1 and sys.argv[1] == '--port' and len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Invalid port number: {}".format(sys.argv[2]))
            sys.exit(1)
    
    app.run(debug=True, port=port) 