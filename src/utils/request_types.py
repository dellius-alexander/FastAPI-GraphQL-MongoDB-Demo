import requests


# -----------------------------------------------------------------------------
def request_get(url: str,
                ext_file_location: str = None,
                params: dict = None,
                headers: dict = None,
                timeout: int = 5,
                ):
    """
    Send a GET request to a URL, download some content and write it to a file, provided an
    external file location is given.

    :param url: The URL to send the request to
    :param ext_file_location: The location to save the file to, i.e. /tmp/file.txt
    :param params: The parameters to send with the request
    :param headers: The headers to send with the request
    :param timeout: The timeout for the request
    :return: The response from the request
    """
    # Send the request
    response = requests.get(url=url, params=params, headers=headers, timeout=timeout)
    file_saved = False
    # Check if the response was successful
    if response.status_code == 200:
        content = response.content
        # Save the file to a local directory
        if ext_file_location is not None:
            with open(ext_file_location, 'wb') as f:
                f.write(content)
                file_saved = True
            # Read the file back in
            with open(ext_file_location, 'rb') as f:
                content = f.read()
        return {"file_saved": file_saved, "status_code": response.status_code, "reason": response.reason, "url": url,
                 "params": params, "headers": headers, "timeout": timeout, "ext_file_location": ext_file_location,
                 "content": content}
    else:
        return {"file_saved": file_saved, "status_code": response.status_code, "reason": response.reason, "url": url,
                 "params": params, "headers": headers, "timeout": timeout, "ext_file_location": ext_file_location}

# -----------------------------------------------------------------------------
