import ssl
import socket

def get_certificate(hostname, port):
    """
    Fetches the certificate data from an endpoint and returns a dictionary.

    Args:
        hostname (str): The hostname of the endpoint.
        port (int): The port number of the endpoint.

    Returns:
        dict or None: The certificate data as a dictionary, or None if an error occurs.
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
    Prints the certificate information in a user-friendly format, excluding
    "subjectAltName" by default and presenting the "subject" key without "commonName".

    Args:
        certificate (dict): The certificate data dictionary.
        sAltName (bool, optional): Whether to print the "subjectAltName" information.
            Defaults to False.
    """

    for key, value in certificate.items():
        if key == "subject":
            print("Subject:")
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
    # print("\n--- OR with subjectAltName ---")
    # print_certificate_info(certificate, sAltName=True)
else:
    print("Failed to retrieve certificate.")