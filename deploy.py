from fabric.api import env, put, run
import os

env.hosts = ['52.86.205.230', '54.146.64.255']
env.user = 'ubuntu'
env.key_filename = 'my_ssh_private_key'


def do_deploy(archive_path):
    # Check if archive_path doesn't exist
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract filename without extension
        filename = os.path.basename(archive_path)
        name, ext = os.path.splitext(filename)
        path = "/data/web_static/releases/{}/".format(name)

        # Uncompress the archive to the folder on the web server
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}".format(filename, path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Move files
        run("mv {}web_static/* {}".format(path, path))
        run("rm -rf {}web_static".format(path))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new the symbolic link /data/web_static/current on the web server
        run("ln -s {} /data/web_static/current".format(path))

        print("New version deployed!")
        return True
    except:
        return False
