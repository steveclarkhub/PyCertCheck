import ssl
import socket

def get_certificate(hostname, port):
    """
    Pulls certificate data from an endpoint. 
    Args: hostname (str) & port (int). Hostname s/b host, ip, fqdn. 
    Returns: The certificate data as a dictionary, or None.
    """

    context = ssl.create_default_context()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((hostname, port))
            connection = context.wrap_socket(sock, server_hostname=hostname)
            certificate = connection.getpeercert()
            return certificate
        except Exception as e:
            print(f"Error fetching certificate: {e}")
            return None


def print_certificate_info(certificate, sAltName=False):
    """
    Prints the certificate information. 
    Unpack "subject" tuple
    Exclude "subjectAltName" (mvp+ optional arg, bool) 
    Args: certificate (dict). subjectAltName False by default
    """

    for key, value in certificate.items():
        if key == "subject":
            print("Subject:")
            for inner_tuple in value:
                for inner_key, inner_value in inner_tuple:
                    print(f"  {inner_key}: {inner_value}")
        elif key == "issuer":
            print("Issuer:")
            for inner_tuple in value:
                for inner_key, inner_value in inner_tuple:
                    print(f"  {inner_key}: {inner_value}")
        elif key != "subjectAltName" or sAltName:
            print(f"{key}: {value}")

# Example usage
hostname = "www.example.com"
port = 443  # Assuming HTTPS

certificate = get_certificate(hostname, port)

if certificate:
    print_certificate_info(certificate)
    # print_certificate_info(certificate, sAltName=True)
else:
    print("Failed to retrieve certificate.")