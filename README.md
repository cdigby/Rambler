# Rambler
A web app for creating and sharing walking and running routes around Guildford based on Django.
## Setup
### Linux
- Install the `docker` and `docker-compose` packages for your distribution.
- Ensure the `docker` service is running on your machine.
- Open the root project directory in a terminal.
- Build the app using `sudo docker-compose build`.
- Perform database migrations using `sudo docker-compose run web python manage.py migrate`.
- Start the app using `sudo docker-compose up`.
- Connect to the app by navigating to `localhost:8000` in your browser.
- Unit tests can be run using `sudo docker-compose run web python manage.py test`

### Windows
- Set up WSL2 on your device. Instructions: https://docs.microsoft.com/en-us/windows/wsl/install-win10
- Install Docker Desktop with the WSL2 backend.
- In Docker Desktop, go to `Settings > Resources > WSL Integration` and enable integration with your distribution. (Tested with Ubuntu)
- Open a WSL terminal in the folder containing the root project folder.
- (Optional) Running the app from a mounted windows directory can cause performance issues, so move the root project folder from wherever it is saved to a location within the WSL home directory.
  - Ideally do this from within the WSL terminal. Accessing `\\wsl$\<distro>\home\<user>` in windows exporer and copying it accross that way should also work but is untested.
- Ensure that Docker Desktop is running and the backend has started.
- In your WSL terminal, navigate to the root project folder.
- Build the app using `docker compose build`.
- Perform database migrations using `docker compose run web python manage.py migrate`.
- Start the app using `docker compose up`.
- Connect to the app by navigating to `localhost:8000` in your browser.
- Unit tests can be run using `docker compose run web python manage.py test`
 
