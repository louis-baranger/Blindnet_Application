
# Blindnet_Application

## How to use: 

### Server:

1. Download Server.py and Server_helper.py
2. Move files to wanted directory
3. Open terminal
4. Change directory to where Server.py and Server_helper.py are located using <em><strong>cd "directory"</strong></em>
5. Start Python script using <em><strong>python3 Server.py</strong></em>
6. Follow the instructions on the terminal

### Client: 

1. Download Client.py and Client_helper.py
2. Move files to wanted directory
3. Open terminal
4. Change directory to where Client.py and Client_helper.py are located using <em><strong>cd "directory"</strong></em>
5. Start Python script using <em><strong>python3 Client.py</strong></em>
6. Follow the instructions on the terminal

### Description: 

<p>
This app supports the encryption of both strings and files. When the Client app starts, the user is asked whether 
he wants to upload data, download data, or change settings. By default, the app uses the "http://localhost:8000" server URL, 
which is the same as the default URL of the Server and will work on a local network. It also downloads files from the Server
in the folder where the Client.py file is located. Both of these settings can be changed in the settings menu.
Basic error checking has been implemented to avoid input errors from the user. 
</p>


<p>
The Client.py file uses the os library to make access and make changes to the file system. This library is also used to generate a
random byte string used during encryption. It also uses the pathlib library to make some of the path manipulation cleaner. 
The cryptography library was chosen for its easy to use interface, its reputation, and its frequent updates. Finally, the
requests library was used to make fomatting http requests cleaner. 
</p>

<p>
By default, the Server app stores files in the folder where Server.py is located. This can be changed when the program is started in the
custom settings menu. The host and port can also be changed in that menu. Both the Server and Client apps are built to work using the 
default settings, as long as they are on the same local network. 
</p>

<p>
The Server.py file overrides the do_GET and do_POST functions from the BaseHTTPRequestHandler in the http.server library to 
make them handle file storage and retrieval correctly. It also uses the os library to access and make changes to the file system. 
Finally, the Server uses the shutil library to allow for the transfer of large files. 
</p>

### Possible future improvements:

<p>
The first improvement that I would make would be some kind of authentication system. As is, the app will accept any file from anyone, 
without limitations to number of requests, size of files and number of files. This could be used by a malicious user to overload the
server. As is, any user can also access any files that have been sent to the server. This is a security flaw because it allows anyone
to download any file and to try to decrypt it through brute force. An authentication system could be used to address both of these 
issues by limiting the rate of requests that can be made by any user, limiting the amount of storage that can be used per user, and 
creating restrictions as to who can download which files. 
</p>


<p>
The next improvement that I would make would be to implement the storage system on the server as a database. The current implementation
uses the file system and creates a .txt file to hold metadata such as the type of file, its name, ... The use of a database would make the
storage folder cleaner and most likely save some disk space in the process. 
</p>

<p>
Finally, I would implement an option for a second disk to be used as backup, or some other kind of data redundency system to ensure that
the server is able to function correctly, even in case of data corruption or data loss. 
</p>
