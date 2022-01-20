# brickbox.io Contributor Workflow

Development is done directly on the server.

General workflow:

1) Ensure pageant is running and your private key has been added.
2) Open Putty to establish a terminal session to the server.
3) Change directory to **/opt/brickbox**
4) Startup the virtual python environment with **source bbenv/bin/activate**

All of the following instrictions are ran from the /opt/brickbox directory with the virtual environment activated unless otherwise noted.

## Static Files

Once ready to deploy the static files, run the following commands:

```bash
python manage.py collectstatic
```

## Update System Files

```bash
systemctl restart gunicorn
```

## Git & GitHub

It is strongly encuranged to make many commits with small changes rather than a single commit with many changes.

Always start by pulling the latest code from the **master** branch in the repository.

```bash
git pull origin master
```

After adding the files you want to commit, run the following command:

```bash
gitcommit
```

This will start a wizard to commit the changes.

Finally run **git push** then visit the GitHub page to verify all workflows have completed successfully before opening a pull request.
